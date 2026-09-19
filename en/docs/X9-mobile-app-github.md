# GitHub Guide for Mobile Developers

> Complete GitHub workflow and CI/CD practices for Android, iOS, Flutter, and React Native developers

---

## Table of Contents

1. [Android Project GitHub Actions CI/CD](#1-android-project-github-actions-cicd)
2. [iOS Project GitHub Actions CI/CD](#2-ios-project-github-actions-cicdxcode-fastlane)
3. [Flutter Project GitHub Actions](#3-flutter-project-github-actions)
4. [React Native Project GitHub Actions](#4-react-native-project-github-actions)
5. [Mobile Automated Testing](#5-mobile-automated-testing)
6. [Code Signing Management](#6-code-signing-management)
7. [App Store Release Automation](#7-app-store-release-automation)
8. [Mobile Code Quality](#8-mobile-code-quality)
9. [Mobile Dependency Management](#9-mobile-dependency-management)
10. [Mobile Crash Monitoring Integration](#10-mobile-crash-monitoring-integration)
11. [Mobile Security Best Practices](#11-mobile-security-best-practices)
12. [Special Configurations for Chinese Developers](#12-special-configurations-for-chinese-developers)

---

## 1. Android Project GitHub Actions CI/CD

### 1.1 Basic Android CI Workflow

For Android projects, GitHub Actions provides powerful automation capabilities. Let's start with a complete basic CI configuration file:

```yaml
# .github/workflows/android-ci.yml
name: Android CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: gradle
      
      - name: Grant execute permission for gradlew
        run: chmod +x gradlew
      
      - name: Build with Gradle
        run: ./gradlew assembleDebug
      
      - name: Run unit tests
        run: ./gradlew testDebugUnitTest
      
      - name: Upload APK artifact
        uses: actions/upload-artifact@v4
        with:
          name: debug-apk
          path: app/build/outputs/apk/debug/app-debug.apk
```

### 1.2 Multi-Module Android Project CI

Large Android projects typically use a multi-module architecture, which requires special handling in CI configuration:

```yaml
# .github/workflows/android-multi-module-ci.yml
name: Android Multi-Module CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      app: ${{ steps.changes.outputs.app }}
      core: ${{ steps.changes.outputs.core }}
      feature: ${{ steps.changes.outputs.feature }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: changes
        with:
          filters: |
            app:
              - 'app/**'
            core:
              - 'core/**'
            feature:
              - 'feature-*/**'

  build-core:
    needs: detect-changes
    if: needs.detect-changes.outputs.core == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: gradle
      - run: ./gradlew :core:build :core:test

  build-features:
    needs: [detect-changes, build-core]
    if: always() && needs.detect-changes.outputs.feature == 'true'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        module: [feature-home, feature-profile, feature-settings]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: gradle
      - run: ./gradlew :${{ matrix.module }}:build :${{ matrix.module }}:test

  build-app:
    needs: [build-core, build-features]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: gradle
      - run: ./gradlew assembleDebug
```

### 1.3 Android Build Cache Optimization

Gradle builds can be very time-consuming. Proper cache configuration can significantly improve CI efficiency:

```yaml
      - name: Cache Gradle packages
        uses: actions/cache@v4
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
          restore-keys: |
            ${{ runner.os }}-gradle-

      - name: Cache AVD
        uses: actions/cache@v4
        id: avd-cache
        with:
          path: |
            ~/.android/avd/*
            ~/.android/adb*
          key: avd-${{ hashFiles('.github/workflows/android-ci.yml') }}
```

---

## 2. iOS Project GitHub Actions CI/CD (Xcode, Fastlane)

### 2.1 Basic iOS CI Workflow

iOS projects must be built in a macOS environment, which is the biggest difference from Android projects:

```yaml
# .github/workflows/ios-ci.yml
name: iOS CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: macos-14
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Select Xcode version
        run: sudo xcode-select -s /Applications/Xcode_15.2.app
      
      - name: Show Xcode version
        run: xcodebuild -version
      
      - name: Resolve package dependencies
        run: xcodebuild -resolvePackageDependencies -scheme MyApp -project MyApp.xcodeproj
      
      - name: Build for testing
        run: |
          xcodebuild build-for-testing \
            -scheme MyApp \
            -project MyApp.xcodeproj \
            -destination 'platform=iOS Simulator,name=iPhone 15,OS=17.2' \
            -derivedDataPath build/ \
            CODE_SIGN_IDENTITY="" \
            CODE_SIGNING_REQUIRED=NO
      
      - name: Run tests
        run: |
          xcodebuild test-without-building \
            -scheme MyApp \
            -project MyApp.xcodeproj \
            -destination 'platform=iOS Simulator,name=iPhone 15,OS=17.2' \
            -derivedDataPath build/ \
            -resultBundlePath TestResults.xcresult
      
      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: TestResults.xcresult
```

### 2.2 Fastlane Integration

Fastlane is a powerful tool for mobile automation releases, and it works exceptionally well with GitHub Actions:

```ruby
# fastlane/Fastfile
default_platform(:ios)

platform :ios do
  desc "Run tests"
  lane :test do
    scan(
      scheme: "MyApp",
      device: "iPhone 15",
      clean: true,
      code_coverage: true
    )
  end

  desc "Build and sign"
  lane :build do |options|
    match(
      type: options[:type] || "development",
      readonly: true
    )
    gym(
      scheme: "MyApp",
      export_method: options[:export_method] || "development",
      clean: true
    )
  end

  desc "Deploy to TestFlight"
  lane :beta do
    build(type: "appstore", export_method: "app-store")
    upload_to_testflight(
      skip_waiting_for_build_processing: true
    )
  end

  desc "Deploy to App Store"
  lane :release do
    build(type: "appstore", export_method: "app-store")
    upload_to_app_store(
      force: true,
      skip_metadata: false,
      skip_screenshots: false
    )
  end
end
```

Calling Fastlane in GitHub Actions:

```yaml
# .github/workflows/ios-fastlane.yml
name: iOS Fastlane

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      
      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_15.2.app
      
      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
      
      - name: Install Fastlane
        run: gem install fastlane
      
      - name: Setup signing
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_URL: ${{ secrets.MATCH_GIT_URL }}
        run: |
          echo "${{ secrets.MATCH_CERTIFICATES_REPO_KEY }}" > match_key
          fastlane match appstore --readonly
      
      - name: Build and deploy
        env:
          APP_STORE_CONNECT_API_KEY: ${{ secrets.APP_STORE_CONNECT_API_KEY }}
        run: fastlane beta
```

### 2.3 Xcode Cloud and GitHub Integration

Xcode Cloud is Apple's CI/CD service that can directly integrate with GitHub repositories:

```yaml
# .github/workflows/xcode-cloud-trigger.yml
name: Trigger Xcode Cloud

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  trigger:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Xcode Cloud build
        run: |
          curl -X POST \
            -H "Authorization: Bearer ${{ secrets.XCODE_CLOUD_TOKEN }}" \
            -H "Content-Type: application/json" \
            "https://api.appstoreconnect.apple.com/v1/ciWorkflows/${{ secrets.WORKFLOW_ID }}/actions/startNewBuild" \
            -d '{"data":{"type":"ciBuildRuns","relationships":{"scmGitReference":{"data":{"type":"scmGitReferences","id":"${{ secrets.BRANCH_ID }}"}}}}}'
```

---

## 3. Flutter Project GitHub Actions

### 3.1 Flutter CI Basic Configuration

Flutter projects need to support building for both Android and iOS platforms:

```yaml
# .github/workflows/flutter-ci.yml
name: Flutter CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.19.0'
          channel: 'stable'
          cache: true
      - run: flutter pub get
      - run: flutter analyze
      - run: flutter format --set-exit-if-changed .

  test:
    runs-on: ubuntu-latest
    needs: analyze
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.19.0'
          channel: 'stable'
          cache: true
      - run: flutter pub get
      - run: flutter test --coverage
      - uses: codecov/codecov-action@v4
        with:
          file: coverage/lcov.info

  build-android:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.19.0'
          channel: 'stable'
          cache: true
      - run: flutter pub get
      - run: flutter build apk --release
      - uses: actions/upload-artifact@v4
        with:
          name: android-release
          path: build/app/outputs/flutter-apk/app-release.apk

  build-ios:
    runs-on: macos-14
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.19.0'
          channel: 'stable'
          architecture: x64
          cache: true
      - run: flutter pub get
      - run: flutter build ios --release --no-codesign
      - uses: actions/upload-artifact@v4
        with:
          name: ios-build
          path: build/ios/iphoneos/Runner.app
```

### 3.2 Flutter Multi-Platform Release

Flutter 3.x supports building for Web, Windows, macOS, Linux, and other platforms:

```yaml
# .github/workflows/flutter-multi-platform.yml
name: Flutter Multi-Platform Build

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            platform: android
            artifact: build/app/outputs/flutter-apk/app-release.apk
          - os: macos-14
            platform: ios
            artifact: build/ios/iphoneos/Runner.app
          - os: ubuntu-latest
            platform: web
            artifact: build/web
          - os: ubuntu-latest
            platform: linux
            artifact: build/linux/x64/release/bundle
          - os: windows-latest
            platform: windows
            artifact: build/windows/x64/runner/Release
          - os: macos-14
            platform: macos
            artifact: build/macos/Build/Products/Release

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.19.0'
          channel: 'stable'
          cache: true
      - run: flutter pub get
      - name: Build ${{ matrix.platform }}
        run: flutter build ${{ matrix.platform }} --release
      - uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.platform }}-release
          path: ${{ matrix.artifact }}
```

---

## 4. React Native Project GitHub Actions

### 4.1 React Native CI Basics

React Native projects need to handle both JavaScript and native layer builds:

```yaml
# .github/workflows/react-native-ci.yml
name: React Native CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  javascript:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'yarn'
      - run: yarn install --frozen-lockfile
      - run: yarn lint
      - run: yarn test --coverage
      - run: yarn tsc --noEmit

  android:
    needs: javascript
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'yarn'
      - run: yarn install --frozen-lockfile
      - name: Build Android
        working-directory: android
        run: ./gradlew assembleDebug
      - uses: actions/upload-artifact@v4
        with:
          name: android-debug
          path: android/app/build/outputs/apk/debug/app-debug.apk

  ios:
    needs: javascript
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'yarn'
      - run: yarn install --frozen-lockfile
      - name: Install CocoaPods
        working-directory: ios
        run: pod install
      - name: Build iOS
        run: |
          xcodebuild -workspace ios/MyApp.xcworkspace \
            -scheme MyApp \
            -configuration Debug \
            -destination 'generic/platform=iOS Simulator' \
            -derivedDataPath ios/build \
            build
```

### 4.2 React Native E2E Testing

End-to-end testing with Detox is a standard practice for React Native projects:

```yaml
# .github/workflows/react-native-e2e.yml
name: React Native E2E Tests

on:
  pull_request:
    branches: [ main ]

jobs:
  e2e-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'yarn'
      - run: yarn install --frozen-lockfile
      - name: Build for Detox
        run: |
          yarn detox build \
            --configuration android.emu.debug
      - name: Run E2E tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          arch: x86_64
          profile: Pixel_6
          script: yarn detox test --configuration android.emu.debug

  e2e-ios:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'yarn'
      - run: yarn install --frozen-lockfile
      - name: Install CocoaPods
        working-directory: ios
        run: pod install
      - name: Build for Detox
        run: yarn detox build --configuration ios.sim.debug
      - name: Run E2E tests
        run: yarn detox test --configuration ios.sim.debug
```

---

## 5. Mobile Automated Testing

### 5.1 Espresso (Android UI Testing)

```kotlin
// android/app/src/androidTest/java/com/myapp/LoginActivityTest.kt
@RunWith(AndroidJUnit4::class)
class LoginActivityTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(LoginActivity::class.java)

    @Test
    fun loginWithValidCredentials_shouldShowDashboard() {
        onView(withId(R.id.et_username))
            .perform(typeText("testuser"), closeSoftKeyboard())
        onView(withId(R.id.et_password))
            .perform(typeText("password123"), closeSoftKeyboard())
        onView(withId(R.id.btn_login))
            .perform(click())
        onView(withId(R.id.tv_welcome))
            .check(matches(isDisplayed()))
            .check(matches(withText("Welcome, testuser")))
    }

    @Test
    fun loginWithEmptyFields_shouldShowError() {
        onView(withId(R.id.btn_login))
            .perform(click())
        onView(withId(R.id.til_username))
            .check(matches(hasDescendant(withText("Username is required"))))
    }
}
```

Running Espresso tests in GitHub Actions:

```yaml
      - name: Run instrumentation tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          arch: x86_64
          profile: Pixel_6
          script: ./gradlew connectedDebugAndroidTest
      
      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: android-test-results
          path: app/build/reports/androidTests/
```

### 5.2 XCTest (iOS UI Testing)

```swift
// ios/MyAppUITests/LoginUITests.swift
import XCTest

class LoginUITests: XCTestCase {
    
    let app = XCUIApplication()
    
    override func setUpWithError() throws {
        continueAfterFailure = false
        app.launch()
    }
    
    func test_loginWithValidCredentials_showsDashboard() {
        let usernameField = app.textFields["usernameTextField"]
        let passwordField = app.secureTextFields["passwordTextField"]
        let loginButton = app.buttons["loginButton"]
        
        usernameField.tap()
        usernameField.typeText("testuser")
        
        passwordField.tap()
        passwordField.typeText("password123")
        
        loginButton.tap()
        
        let welcomeLabel = app.staticTexts["welcomeLabel"]
        XCTAssertTrue(welcomeLabel.waitForExistence(timeout: 5))
        XCTAssertEqual(welcomeLabel.label, "Welcome, testuser")
    }
    
    func test_loginWithEmptyFields_showsError() {
        app.buttons["loginButton"].tap()
        
        let errorLabel = app.staticTexts["usernameError"]
        XCTAssertTrue(errorLabel.waitForExistence(timeout: 2))
    }
}
```

### 5.3 Detox (React Native E2E Testing)

```javascript
// e2e/login.test.js
describe('Login Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('should login successfully with valid credentials', async () => {
    await element(by.id('username-input')).typeText('testuser');
    await element(by.id('password-input')).typeText('password123');
    await element(by.id('login-button')).tap();
    await expect(element(by.id('welcome-text'))).toBeVisible();
    await expect(element(by.id('welcome-text'))).toHaveText('Welcome, testuser');
  });

  it('should show error with empty fields', async () => {
    await element(by.id('login-button')).tap();
    await expect(element(by.id('username-error'))).toBeVisible();
  });
});
```

---

## 6. Code Signing Management

### 6.1 Android Keystore Management

Secure management of Android signing keys is crucial:

```yaml
# .github/workflows/android-sign.yml
name: Android Signed Build

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Decode Keystore
        run: |
          echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > app/release.keystore

      - name: Build signed APK
        env:
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
        run: |
          ./gradlew assembleRelease \
            -Pandroid.injected.signing.store.file=release.keystore \
            -Pandroid.injected.signing.store.password=$KEYSTORE_PASSWORD \
            -Pandroid.injected.signing.key.alias=$KEY_ALIAS \
            -Pandroid.injected.signing.key.password=$KEY_PASSWORD

      - name: Clean up keystore
        if: always()
        run: rm -f app/release.keystore
```

### 6.2 iOS Provisioning Profile Management

Using Fastlane Match to manage iOS certificates and provisioning profiles:

```yaml
      - name: Setup iOS signing
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          FASTLANE_USER: ${{ secrets.FASTLANE_USER }}
          FASTLANE_PASSWORD: ${{ secrets.FASTLANE_PASSWORD }}
        run: |
          # Decode certificates from Secrets
          echo "${{ secrets.DIST_CERT_BASE64 }}" | base64 -d > distribution.p12
          echo "${{ secrets.PROVISION_PROFILE_BASE64 }}" | base64 -d > profile.mobileprovision
          
          # Import certificate to Keychain
          security create-keychain -p "" build.keychain
          security import distribution.p12 \
            -k build.keychain \
            -P "${{ secrets.P12_PASSWORD }}" \
            -T /usr/bin/codesign
          security set-keychain-settings build.keychain
          security list-keychains -s build.keychain
          
          # Install provisioning profile
          mkdir -p ~/Library/MobileDevice/Provisioning\ Profiles
          cp profile.mobileprovision \
            ~/Library/MobileDevice/Provisioning\ Profiles/
```

### 6.3 Key Rotation Strategy

```yaml
# .github/workflows/key-rotation-check.yml
name: Key Rotation Check

on:
  schedule:
    - cron: '0 0 1 * *'  # Check monthly

jobs:
  check-keys:
    runs-on: ubuntu-latest
    steps:
      - name: Check Android keystore age
        run: |
          # Check keystore creation time, send notification if over 1 year
          CREATED=$(gh api repos/${{ github.repository }}/actions/secrets/KEYSTORE_CREATED_AT --jq '.value' 2>/dev/null || echo "unknown")
          echo "Keystore created at: $CREATED"
          
      - name: Create rotation issue
        if: success()
        run: |
          gh issue create \
            --title "Key Rotation Reminder" \
            --body "Please review and rotate signing keys if necessary." \
            --label "security"
```

---

## 7. App Store Release Automation

### 7.1 Google Play Release

Using the `r0adkll/upload-google-play` Action to automatically publish to Google Play:

```yaml
# .github/workflows/google-play-release.yml
name: Google Play Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Build AAB
        env:
          KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
        run: |
          echo "$KEYSTORE_BASE64" | base64 -d > app/release.keystore
          ./gradlew bundleRelease \
            -Pandroid.injected.signing.store.file=release.keystore \
            -Pandroid.injected.signing.store.password=$KEYSTORE_PASSWORD \
            -Pandroid.injected.signing.key.alias=$KEY_ALIAS \
            -Pandroid.injected.signing.key.password=$KEY_PASSWORD

      - name: Upload to Google Play
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.GOOGLE_PLAY_SERVICE_ACCOUNT_JSON }}
          packageName: com.mycompany.myapp
          releaseFiles: app/build/outputs/bundle/release/app-release.aab
          track: production
          status: completed
          releaseNotes: |
            -en-US: Bug fixes and performance improvements
            -zh-CN: 修复问题和性能改进
```

### 7.2 App Store Release

```yaml
# .github/workflows/app-store-release.yml
name: App Store Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true

      - name: Setup signing
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
        run: fastlane match appstore --readonly

      - name: Build and upload
        run: fastlane release
        env:
          APP_STORE_CONNECT_API_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          APP_STORE_CONNECT_API_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY: ${{ secrets.ASC_PRIVATE_KEY }}
```

### 7.3 Domestic App Market Release

The domestic market has many channels, requiring special multi-channel packaging solutions:

```yaml
# .github/workflows/china-market-release.yml
name: China Market Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-channels:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        channel: [huawei, xiaomi, oppo, vivo, tencent]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Build channel APK
        run: |
          ./gradlew assembleRelease \
            -Pchannel=${{ matrix.channel }}

      - name: Upload channel artifact
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.channel }}-release
          path: app/build/outputs/apk/release/*-${{ matrix.channel }}-release.apk

  upload-to-markets:
    needs: build-channels
    runs-on: ubuntu-latest
    steps:
      - name: Upload to Huawei AppGallery
        run: |
          curl -X POST "https://connect-api.cloud.huawei.com/api/publish/v2/uploadFile" \
            -H "Authorization: Bearer ${{ secrets.HUAWEI_TOKEN }}" \
            -F "file=@huawei-release.apk"

      - name: Upload to Tencent App Store
        run: |
          curl -X POST "https://api.open.qq.com/api/upload" \
            -H "Authorization: Bearer ${{ secrets.TENCENT_TOKEN }}" \
            -F "file=@tencent-release.apk"
```

---

## 8. Mobile Code Quality

### 8.1 Android Lint Configuration

```yaml
# .github/workflows/android-lint.yml
name: Android Code Quality

on:
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Run Android Lint
        run: ./gradlew lintDebug

      - name: Run ktlint
        run: |
          ./gradlew ktlintCheck

      - name: Run detekt
        run: |
          ./gradlew detekt

      - name: Upload lint results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: lint-results
          path: app/build/reports/lint-results-debug.html
```

detekt configuration file:

```yaml
# config/detekt/detekt.yml
complexity:
  LongMethod:
    threshold: 60
  LongParameterList:
    functionThreshold: 6
    constructorThreshold: 7
  ComplexMethod:
    threshold: 15

style:
  MaxLineLength:
    maxLineLength: 120
  MagicNumber:
    active: false

naming:
  FunctionNaming:
    functionPattern: '[a-z][a-zA-Z0-9]*'
```

### 8.2 SwiftLint Configuration

```yaml
# .github/workflows/swiftlint.yml
name: SwiftLint

on:
  pull_request:
    paths:
      - '**/*.swift'

jobs:
  swiftlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run SwiftLint
        uses: norio-nomura/action-swiftlint@3.2.1
        with:
          args: --strict
```

`.swiftlint.yml` configuration:

```yaml
# .swiftlint.yml
excluded:
  - Pods
  - DerivedData
  - .build

disabled_rules:
  - trailing_whitespace

opt_in_rules:
  - empty_count
  - closure_spacing
  - force_unwrapping

line_length:
  warning: 120
  error: 200

type_body_length:
  warning: 300
  error: 500

file_length:
  warning: 500
  error: 1000

identifier_name:
  min_length:
    warning: 2
  max_length:
    warning: 60
```

---

## 9. Mobile Dependency Management

### 9.1 Android Dependency Management

Using Gradle Version Catalog to centrally manage dependency versions:

```toml
# gradle/libs.versions.toml
[versions]
kotlin = "1.9.22"
compose = "1.6.0"
coroutines = "1.7.3"
room = "2.6.1"
retrofit = "2.9.0"
okhttp = "4.12.0"

[libraries]
compose-ui = { module = "androidx.compose.ui:ui", version.ref = "compose" }
compose-material3 = { module = "androidx.compose.material3:material3", version.ref = "compose" }
room-runtime = { module = "androidx.room:room-runtime", version.ref = "room" }
room-compiler = { module = "androidx.room:room-compiler", version.ref = "room" }
retrofit = { module = "com.squareup.retrofit2:retrofit", version.ref = "retrofit" }
okhttp-logging = { module = "com.squareup.okhttp3:logging-interceptor", version.ref = "okhttp" }

[plugins]
android-application = { id = "com.android.application", version = "8.2.2" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
```

Dependency security check:

```yaml
# .github/workflows/dependency-check.yml
name: Dependency Security Check

on:
  schedule:
    - cron: '0 0 * * 1'  # Check every Monday

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Check Android dependencies
        run: ./gradlew dependencyCheckAnalyze

      - name: Create issue on vulnerabilities
        if: failure()
        run: |
          gh issue create \
            --title "Dependency vulnerabilities detected" \
            --body "OWASP dependency check found vulnerabilities. Please review." \
            --label "security,dependencies"
```

### 9.2 iOS CocoaPods/Swift Package Manager

```yaml
# .github/workflows/ios-dependency-cache.yml
      - name: Cache CocoaPods
        uses: actions/cache@v4
        with:
          path: ios/Pods
          key: ${{ runner.os }}-pods-${{ hashFiles('ios/Podfile.lock') }}
          restore-keys: |
            ${{ runner.os }}-pods-

      - name: Cache SPM
        uses: actions/cache@v4
        with:
          path: |
            ~/Library/Caches/org.swift.swiftpm
            .build
          key: ${{ runner.os }}-spm-${{ hashFiles('Package.resolved') }}
```

---

## 10. Mobile Crash Monitoring Integration

### 10.1 Firebase Crashlytics Integration

```yaml
# .github/workflows/firebase-crashlytics.yml
      - name: Upload dSYMs to Firebase
        run: |
          find ~/Library/Developer/Xcode/DerivedData -name "*.dSYM" | \
          while read dsym; do
            ${{ github.workspace }}/Pods/FirebaseCrashlytics/upload-symbols \
              -gsp ${{ github.workspace }}/GoogleService-Info.plist \
              -p ios \
              "$dsym"
          done

      - name: Upload Android mapping file
        run: |
          ./gradlew uploadCrashlyticsMappingFileRelease
```

### 10.2 Sentry Integration

```yaml
# .github/workflows/sentry-release.yml
name: Sentry Release

on:
  push:
    tags:
      - 'v*'

jobs:
  sentry-release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Sentry CLI
        run: npm install -g @sentry/cli

      - name: Create Sentry release
        env:
          SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
          SENTRY_ORG: my-org
          SENTRY_PROJECT: my-app
        run: |
          RELEASE_VERSION="${GITHUB_REF#refs/tags/}"
          
          # Create release
          sentry-cli releases new "$RELEASE_VERSION"
          sentry-cli releases set-commits "$RELEASE_VERSION" --auto
          
          # Upload iOS dSYMs
          sentry-cli upload-dif --org $SENTRY_ORG \
            --project $SENTRY_PROJECT \
            path/to/dSYMs
          
          # Upload Android mapping
          sentry-cli upload-proguard \
            --android-manifest app/build/outputs/mapping/release/AndroidManifest.xml \
            app/build/outputs/mapping/release/mapping.txt
          
          # Finalize release
          sentry-cli releases finalize "$RELEASE_VERSION"
```

### 10.3 Bugly Integration (Tencent)

Domestic projects commonly use Tencent Bugly for crash monitoring:

```yaml
      - name: Upload mapping to Bugly
        run: |
          curl -X POST "https://api.bugly.qq.com/openapi/file/upload/symbol" \
            -F "app_id=${{ secrets.BUGLY_APP_ID }}" \
            -F "app_key=${{ secrets.BUGLY_APP_KEY }}" \
            -F "symbolType=Android" \
            -F "bundleId=com.mycompany.myapp" \
            -F "productVersion=${GITHUB_REF#refs/tags/}" \
            -F "channel=tencent" \
            -F "fileName=mapping.txt" \
            -F "file=@app/build/outputs/mapping/release/mapping.txt"
```

---

## 11. Mobile Security Best Practices

### 11.1 Secrets Scanning

```yaml
# .github/workflows/secrets-scan.yml
name: Secrets Scan

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 11.2 Dependency Vulnerability Scanning

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  schedule:
    - cron: '0 0 * * *'

jobs:
  android-security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - name: OWASP Dependency Check
        run: ./gradlew dependencyCheckAnalyze

  ios-security:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      - name: Audit CocoaPods
        run: |
          gem install bundler-audit
          cd ios && bundle-audit check --update
```

### 11.3 Code Obfuscation Check

```yaml
      - name: Verify ProGuard configuration
        run: |
          if ! grep -q "minifyEnabled true" app/build.gradle; then
            echo "Warning: minification is not enabled for release build"
            exit 1
          fi
          
          if ! grep -q "shrinkResources true" app/build.gradle; then
            echo "Warning: resource shrinking is not enabled"
            exit 1
          fi
```

---

## 12. Special Configurations for Chinese Developers

### 12.1 Gradle Domestic Mirror Configuration

```groovy
// settings.gradle.kts (project-level)
pluginManagement {
    repositories {
        maven("https://maven.aliyun.com/repository/gradle-plugin")
        maven("https://maven.aliyun.com/repository/google")
        maven("https://maven.aliyun.com/repository/central")
        maven("https://maven.aliyun.com/repository/public")
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositories {
        maven("https://maven.aliyun.com/repository/google")
        maven("https://maven.aliyun.com/repository/central")
        maven("https://maven.aliyun.com/repository/public")
        google()
        mavenCentral()
    }
}
```

### 12.2 npm/Flutter Domestic Mirrors

```yaml
# .github/workflows/flutter-china-mirror.yml
      - name: Setup Flutter with China mirror
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.19.0'
          channel: 'stable'
        env:
          PUB_HOSTED_URL: https://pub.flutter-io.cn
          FLUTTER_STORAGE_BASE_URL: https://storage.flutter-io.cn

      - name: Setup npm China mirror
        run: |
          npm config set registry https://registry.npmmirror.com
          yarn config set registry https://registry.npmmirror.com
```

### 12.3 GitHub Actions Acceleration Configuration

```yaml
# Using domestic server self-hosted Runner solution
# .github/workflows/self-hosted-runner.yml
name: Self-Hosted Runner Build

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: [self-hosted, linux, x64]  # Use self-hosted Runner
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - name: Build with Gradle
        run: |
          # Set up domestic Gradle mirror
          mkdir -p ~/.gradle
          cat > ~/.gradle/init.d/mirror.gradle << 'EOF'
          allprojects {
            repositories {
              maven { url 'https://maven.aliyun.com/repository/google' }
              maven { url 'https://maven.aliyun.com/repository/central' }
              maven { url 'https://maven.aliyun.com/repository/public' }
            }
          }
          EOF
          ./gradlew assembleDebug
```

### 12.4 GitHub Access Acceleration Solutions

```yaml
# Using GitHub proxy solution
# .github/workflows/ghproxy.yml
      - name: Setup with GitHub proxy
        run: |
          # Configure Git to use ghproxy
          git config --global url."https://ghproxy.com/https://github.com/".insteadOf "https://github.com/"
          
          # Configure Go module proxy
          go env -w GOPROXY=https://goproxy.cn,direct
          
          # Configure Rust crates mirror
          mkdir -p ~/.cargo
          cat > ~/.cargo/config.toml << 'EOF'
          [source.crates-io]
          replace-with = 'ustc'
          [source.ustc]
          registry = "sparse+https://mirrors.ustc.edu.cn/crates.io-index/"
          EOF
```

### 12.5 Domestic CI/CD Service Integration

In addition to GitHub Actions, domestic developers can also consider using the following CI/CD services:

- **Gitee Go**: CI/CD service provided by Gitee
- **Alibaba Cloud DevOps**: Alibaba's DevOps platform
- **Tencent Cloud CODING**: Tencent's CI/CD platform
- **Huawei Cloud DevCloud**: Huawei's DevOps service

These services have fast access speeds in China and better integration with domestic app markets.

---

## Summary

This guide covers the core aspects of project management on GitHub for mobile developers:

| Topic | Key Points |
|-------|------------|
| CI/CD | Complete workflow configurations for different tech stacks |
| Automated Testing | Practical applications of Espresso, XCTest, Detox |
| Code Signing | Secure management of signing certificates and keys |
| App Release | Automated publishing to Google Play, App Store, and domestic markets |
| Code Quality | Configuration and usage of Lint and static analysis tools |
| Security Practices | Dependency vulnerability scanning, key leak prevention |
| Domestic Optimization | Mirror configuration, access acceleration solutions |

Mobile CI/CD is a complex but extremely important field. Proper GitHub Actions configuration can significantly improve development efficiency, reduce human errors, and ensure application quality. It is recommended to start with basic configurations and gradually improve your mobile CI/CD workflow.

---

*Last updated: September 2026*