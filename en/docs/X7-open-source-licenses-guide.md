# Complete Open Source License Guide

> **Target Audience**: Chinese developers, open source project maintainers, enterprise legal and technical managers
> **Estimated Reading Time**: 45 minutes
> **Prerequisites**: Basic Git and GitHub experience

---

## Table of Contents

1. [Why Open Source Licenses Matter](#1-why-open-source-licenses-matter)
2. [MIT License Deep Dive (Permissive)](#2-mit-license-deep-dive-permissive)
3. [Apache License 2.0 Deep Dive (Permissive + Patent Protection)](#3-apache-license-20-deep-dive-permissive--patent-protection)
4. [BSD License Family (2-Clause, 3-Clause)](#4-bsd-license-family-2-clause-3-clause)
5. [GPL Family (GPLv2, GPLv3, AGPLv3) Deep Dive](#5-gpl-family-gplv2-gplv3-agplv3-deep-dive)
6. [LGPL Deep Dive](#6-lgpl-deep-dive)
7. [MPL 2.0 (Mozilla Public License)](#7-mpl-20mozilla-public-license)
8. [Creative Commons Licenses](#8-creative-commons-licenses)
9. [License Compatibility Matrix](#9-license-compatibility-matrix)
10. [How to Choose an Open Source License (Decision Tree)](#10-how-to-choose-an-open-source-license-decision-tree)
11. [Dual Licensing and Commercial Licensing](#11-dual-licensing-and-commercial-licensing)
12. [Legal Issues of Open Source Licenses](#12-legal-issues-of-open-source-licenses)
13. [LICENSE File and SPDX Identifiers](#13-license-file-and-spdx-identifiers)
14. [Chinese Enterprise Open Source Compliance Guide](#14-chinese-enterprise-open-source-compliance-guide)
15. [Common License Misconceptions](#15-common-license-misconceptions)

---

## 1. Why Open Source Licenses Matter

### 1.1 The Nature of Open Source Licenses

An open source license is a legal permission document that defines how others can use, modify, and distribute your code. Without a license, code legally means "All Rights Reserved" and others have no right to use it.

Many beginners have a fatal misconception: **"I put my code on GitHub, so it's open source."** In fact, if you don't explicitly declare an open source license in your repository, under the Berne Convention and copyright laws of various countries, all copyrights are reserved by default. Others:

- Cannot copy your code
- Cannot use your code in their own projects
- Cannot modify and redistribute your code
- Cannot even fork your repository for commercial purposes

### 1.2 Legal Basis of Open Source Licenses

The legal force of open source licenses is based on the following legal principles:

**Copyright Law**: Code, as a literary work, is protected by copyright law. Developers automatically hold the copyright to their code without needing to register.

**Contract Law**: In many jurisdictions, open source licenses are treated as contracts. Users indicate acceptance of the license terms by using the code.

**"Access Equals Authorization" Principle**: In some legal systems, open source licenses are treated as "non-exclusive licenses." When users access the code and use it according to license requirements, an authorization relationship is established.

### 1.3 Core Rights of Open Source Licenses

All open source licenses revolve around the following four core rights:

| Right | Description | English Term |
|------|------|----------|
| Right to Use | Allows anyone to run the software for any purpose | Right to Use |
| Right to Modify | Allows modification of source code | Right to Modify |
| Right to Distribute | Allows distribution of the software to others | Right to Distribute |
| Right to Create Derivative Works | Allows creating derivative works based on the original work | Right to Create Derivative Works |

### 1.4 License Classification Overview

Open source licenses are generally divided into three major categories:

```
Open Source Licenses
├── Permissive
│   ├── MIT License
│   ├── BSD 2-Clause / 3-Clause
│   ├── Apache License 2.0
│   └── ISC License
├── Weak Copyleft
│   ├── LGPL v2.1 / v3
│   ├── MPL 2.0
│   └── EPL 2.0
└── Strong Copyleft
    ├── GPL v2
    ├── GPL v3
    └── AGPL v3
```

### 1.5 Risks of No License

If you publish code on GitHub without adding any license file:

- **Legal Risk**: Anyone who uses your code could be sued because there is no authorization
- **Business Risk**: Companies are reluctant to use your code because the legal status is unclear
- **Community Risk**: Contributors don't know how their code will be used and are unwilling to participate
- **Reputation Risk**: In the open source community, projects without licenses are generally considered unprofessional

---

## 2. MIT License Deep Dive (Permissive)

### 2.1 Full License Text

MIT License is one of the simplest and most popular open source licenses. Its full text is very short:

```
MIT License

Copyright (c) <year> <copyright holders>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 2.2 Core Terms Explained

The core content of MIT License can be summarized in three sentences:

1. **Granting Broad Rights**: Anyone may use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software free of charge
2. **Only Condition**: Retain the copyright notice and permission notice in all copies or substantial portions
3. **Disclaimer**: The software is provided "as is" without any warranty

### 2.3 Use Cases

MIT License is particularly suitable for the following scenarios:

- **Tools and Frameworks**: Such as jQuery, React, Vue.js, Babel, etc.
- **Personal Projects**: Individual developers who want their code to be widely used
- **Enterprise-Friendly Projects**: Projects that want to lower the barrier for enterprise adoption
- **Frontend Ecosystem**: Over 70% of packages in the npm ecosystem use MIT License

### 2.4 Notable MIT Projects

| Project | Domain | GitHub Stars |
|------|------|-------------|
| React | Frontend Framework | 220k+ |
| Vue.js | Frontend Framework | 200k+ |
| jQuery | JavaScript Library | 59k+ |
| Rails | Web Framework | 55k+ |
| Node.js | Runtime | 100k+ |
| .NET Core | Development Framework | 70k+ |

### 2.5 Pros and Cons of MIT License

**Pros**:
- Simple and clear, easy to understand
- Very few restrictions, enterprise-friendly
- Excellent compatibility, can be mixed with code from almost any other license
- High community acceptance

**Cons**:
- No patent protection (this is the main difference from Apache 2.0)
- Does not require derivative works to be open source (may lead to code being used in closed-source projects)
- Does not require attribution to the original author (only requires retaining copyright notice)
- No explicit contributor authorization terms

### 2.6 Using MIT License in Your Project

Steps to add MIT License to a GitHub project:

```bash
# 1. Create LICENSE file in project root
touch LICENSE

# 2. Write the full MIT license text to the file, replacing year and copyright holder
echo "MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE." > LICENSE

# 3. Add license notice in README.md
echo "## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details." >> README.md
```

---

## 3. Apache License 2.0 Deep Dive (Permissive + Patent Protection)

### 3.1 License Overview

Apache License 2.0 is maintained by the Apache Software Foundation (ASF) and is the preferred license for enterprise-level open source projects. It adds **patent authorization** and **contributor agreement** protections on top of MIT.

### 3.2 Core Terms

Key terms of Apache 2.0 include:

**Patent Authorization**: Contributors explicitly grant users a free, irrevocable patent license covering patent claims that are necessarily infringed by their contributions. This is Apache 2.0's biggest advantage over MIT.

**Trademark Protection**: The license does not grant rights to use project trademarks, service marks, or product names.

**Contributor Statement**: If users modify the code, they must add a prominent statement in the modified files.

**NOTICE File**: If the original work contains a NOTICE file, derivative works must include a readable copy of that file.

**Distribution Requirements**: When distributing, you must:
- Give recipients a copy of this license
- Add statements in modified files
- Retain all copyright, patent, trademark, and attribution notices
- Include the NOTICE file content if applicable

### 3.3 Patent Terms Explained

Apache 2.0's patent terms are its most important feature:

```
Subject to the terms and conditions of this License, each Contributor hereby
grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free,
irrevocable patent license to make, have made, use, offer to sell, sell,
import, and otherwise transfer the Work, where such license applies only to
those patent claims licensable by such Contributor that are necessarily
infringed by their Contribution(s) alone or by combination of their
Contribution(s) with the Work to which such Contribution(s) was submitted.
```

This means:
- If you contribute code, you grant users the right to use your related patents
- This authorization is perpetual, worldwide, and irrevocable
- If you sue users for patent infringement, your patent license will be automatically terminated (patent retaliation clause)

### 3.4 Patent Retaliation Clause

Apache 2.0 contains a "Patent Retaliation" clause:

```
If You institute patent litigation against any entity (including a
cross-claim or counterclaim in a lawsuit) alleging that the Work or a
Contribution incorporated within the Work constitutes direct or contributory
patent infringement, then any patent licenses granted to You under this
License for that Work shall terminate as of the date such litigation is filed.
```

This effectively prevents "patent trolling": if you use Apache 2.0 code and then sue the original project for patent infringement, you will lose the right to use that code.

### 3.5 Notable Apache 2.0 Projects

| Project | Domain | Description |
|------|------|------|
| Kubernetes | Container Orchestration | Cloud-native infrastructure |
| Android | Mobile Operating System | Maintained by Google |
| Apache Kafka | Message Queue | Stream processing platform |
| TensorFlow | Machine Learning | Open sourced by Google |
| Swift | Programming Language | Open sourced by Apple |
| Elasticsearch | Search Engine | Full-text search |

### 3.6 Apache 2.0 vs MIT Comparison

| Feature | MIT | Apache 2.0 |
|------|-----|------------|
| Patent Protection | No | Yes |
| Trademark Protection | No | Yes |
| Contributor Statement | Not Required | Required |
| NOTICE File | No | Yes |
| License Length | Short (~170 words) | Long (~4500 words) |
| Enterprise Friendliness | High | Higher |
| Learning Cost | Low | Medium |

---

## 4. BSD License Family (2-Clause, 3-Clause)

### 4.1 BSD License History

BSD (Berkeley Software Distribution) license originated at the University of California, Berkeley and is one of the earliest open source licenses. The BSD family has multiple versions, with 2-Clause and 3-Clause being the most commonly used.

### 4.2 BSD 2-Clause (Simplified BSD)

BSD 2-Clause is the most simplified BSD license, very similar to MIT:

```
BSD 2-Clause License

Copyright (c) <year>, <copyright holder>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.
```

### 4.3 BSD 3-Clause (New BSD)

BSD 3-Clause adds a "non-endorsement" clause:

```
BSD 3-Clause License

Copyright (c) <year>, <copyright holder>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES...
```

The core meaning of the third clause: **Without permission, you cannot use the original author's or contributors' names to promote your products**.

### 4.4 BSD License Family Comparison

| Version | Clauses | Non-Endorsement Clause | Usage Examples |
|------|--------|-----------|----------|
| BSD 0-Clause | 0 | No | Ultra-permissive |
| BSD 1-Clause | 1 | No | Simple attribution statement |
| BSD 2-Clause | 2 | No | FreeBSD, Nginx |
| BSD 3-Clause | 3 | Yes | Django, LLVM |

### 4.5 Notable BSD Projects

- **FreeBSD**: Operating System
- **Nginx**: Web Server (uses BSD 2-Clause)
- **Django**: Python Web Framework (uses BSD 3-Clause)
- **LLVM**: Compiler Infrastructure (uses Apache 2.0 with LLVM Exceptions)
- **Go Standard Library**: Uses BSD 3-Clause

---

## 5. GPL Family (GPLv2, GPLv3, AGPLv3) Deep Dive

### 5.1 Philosophical Foundation of GPL

GPL (GNU General Public License) was created by Richard Stallman and the Free Software Foundation (FSF), based on the "free software" philosophy. GPL's core philosophy is **"copyleft"** (the opposite application of copyright):

> You are free to use, modify, and distribute GPL software, but your derivative works must also be released under the GPL license.

This is what's known as the **"Viral Nature"**: the "freedom" of GPL code "infects" all derivative works.

### 5.2 GPLv2 Explained

GPLv2 was released in 1991 and is the license used by the Linux kernel. Core terms:

**Four Freedoms**:
- Freedom 0: The freedom to run the program for any purpose
- Freedom 1: The freedom to study how the program works and modify it
- Freedom 2: The freedom to redistribute copies
- Freedom 3: The freedom to improve the program and release improvements to the public

**Viral Requirements**:
```
You must cause any work that you distribute or publish, that in whole or in
part contains or is derived from the Program or any part thereof, to be
licensed as a whole at no charge to all third parties under the terms of
this License.
```

**Source Code Obligation**:
- When distributing binary files, you must also provide source code or a written offer to obtain source code
- Source code must be provided in a "machine-readable" form

### 5.3 GPLv3 Explained

GPLv3 was released in 2007 and mainly added the following:

**Anti-Tivoization Clause**: TiVo used GPL code but prevented users from running modified versions through hardware locks. GPLv3 requires providing "Installation Information" to allow users to install modified versions on devices.

**Patent Protection**: Similar to Apache 2.0, contributors grant users explicit patent licenses.

**Anti-DRM Clause**: GPLv3 clearly states that "Digital Restrictions Management" (DRM) based on GPL software does not constitute effective technical protection measures.

**Internationalization Improvements**: Better adaptation to legal systems in different countries.

**Compatibility Improvements**: Added compatibility with Apache 2.0.

### 5.4 AGPLv3 Explained

AGPLv3 (GNU Affero General Public License) addresses the "network use" loophole:

**Problem**: GPL requires providing source code when distributing software, but providing services over a network (SaaS) does not count as "distribution." Therefore, companies can modify GPL code and provide services over a network without releasing the modified source code.

**AGPL's Solution**:
```
Notwithstanding any other provision of this License, if you modify the
Program, your modified version must prominently offer all users interacting
with it remotely through a computer network (if your version supports such
interaction) an opportunity to receive the Corresponding Source of your
version...
```

**Use Cases**:
- SaaS platforms
- Online API services
- Cloud service backends

**Notable AGPL Projects**:
- MongoDB (early versions)
- Nextcloud
- Grafana (early versions)
- Mastodon

### 5.5 GPL Family Comparison

| Feature | GPLv2 | GPLv3 | AGPLv3 |
|------|-------|-------|--------|
| Release Year | 1991 | 2007 | 2007 |
| Anti-Tivoization | No | Yes | Yes |
| Patent Protection | Implied | Explicit | Explicit |
| Network Use | Not Triggered | Not Triggered | Triggered |
| Compatible with Apache 2.0 | No | Yes | Yes |
| Linux Kernel | Yes | No | No |

### 5.6 Practical Impact of GPL Viral Nature

**What causes GPL "infection"**:
- Statically linking to GPL libraries
- Directly calling GPL code
- Copying GPL code into your project

**What does not cause GPL "infection"**:
- Calling GPL programs through independent processes (like command-line tools)
- Using GPL tools to generate output (programs compiled with GCC are not bound by GPL)
- Calling through network APIs (except AGPL)

---

## 6. LGPL Deep Dive

### 6.1 LGPL's Positioning

LGPL (GNU Lesser General Public License) is a "weakened" version of GPL, specifically designed for **libraries**. It allows closed-source software to link to LGPL libraries without requiring the entire software to be open source.

### 6.2 Core Terms of LGPL

**Allowing Closed-Source Linking**:
- You can use LGPL libraries in closed-source software
- But you must: Allow users to replace the LGPL library version
- You must provide object files or source code of the LGPL library

**Modifying LGPL Libraries**:
- If you modify the LGPL library itself, the modified library must be released under LGPL
- Your application can remain closed source

### 6.3 Technical Requirements of LGPL

**Dynamic Linking**: The best practice is to use LGPL libraries through dynamic linking (.so, .dll, .dylib). This allows users to easily replace the library version.

**Static Linking**: If you statically link, you must:
- Provide application object files (.o files)
- Or provide complete source code
- Allow users to relink the application

### 6.4 LGPL Versions

| Version | Description | Usage Examples |
|------|------|----------|
| LGPL v2 | Initial version | GTK+ 2 |
| LGPL v2.1 | Minor improvements | glibc |
| LGPL v3 | Based on GPLv3, adds patent protection | GTK+ 3 |

### 6.5 Notable LGPL Projects

- **glibc**: GNU C Standard Library
- **GTK+**: GUI Library
- **FFmpeg**: Multimedia Processing Library
- **Qt** (partial modules): Cross-platform GUI Framework
- **FFTW**: Fast Fourier Transform Library

### 6.6 LGPL vs GPL Comparison

| Feature | GPL | LGPL |
|------|-----|------|
| Closed-Source Software Can Link | No | Yes |
| Modified Libraries Must Be Open Source | Yes | Yes (library only) |
| Viral Nature | Strong | Weak (library only) |
| Use Cases | Applications | Libraries |

---

## 7. MPL 2.0 (Mozilla Public License)

### 7.1 MPL 2.0 Overview

MPL 2.0 (Mozilla Public License 2.0) is a license maintained by the Mozilla Foundation, used for projects like Firefox and Thunderbird. It is a **file-level** weak copyleft license.

### 7.2 Core Terms

**File-Level Viral Nature**:
- If you modify files covered by MPL, the modified files must be released under MPL 2.0
- You can mix MPL and non-MPL code in the same project
- New files can use any license

**Compatibility with Other Licenses**:
```
This License gives you permission to combine Covered Software with other
software that is not Covered Software, to create a Larger Work, and to
distribute the Larger Work under the terms of your choice.
```

**Patent Authorization**: Similar to Apache 2.0, contributors grant users explicit patent licenses.

**Secondary Licensing**: MPL 2.0 allows code to be simultaneously released under GPL, LGPL, or Apache 2.0.

### 7.3 Advantages of MPL 2.0

1. **Flexibility**: Allows mixing code with different licenses in the same project
2. **File-Level Control**: More moderate than GPL's "project-level" viral nature
3. **Enterprise-Friendly**: Allows commercial software to include MPL code
4. **Patent Protection**: Clear patent authorization terms

### 7.4 Notable MPL 2.0 Projects

- **Firefox**: Web Browser
- **Thunderbird**: Email Client
- **LibreOffice**: Office Suite (uses MPL 2.0)
- **Signal**: Encrypted Messaging App (early versions)

---

## 8. Creative Commons Licenses

### 8.1 CC License Overview

Creative Commons (CC) licenses are mainly used for **non-software works**, such as documents, images, music, videos, etc. Although CC licenses are not recommended for software, they are commonly used for documentation and resource files in open source projects.

### 8.2 CC License Elements

| Element | Abbreviation | Description |
|------|------|------|
| Attribution | BY | Must credit the original author |
| ShareAlike | SA | Derivative works must use the same license |
| NonCommercial | NC | Cannot be used for commercial purposes |
| NoDerivatives | ND | Cannot modify the original work |

### 8.3 CC License Combinations

| License | Full Name | Description |
|------|------|------|
| CC0 | | Public Domain, waives all rights |
| CC BY | Attribution 4.0 | Only requires attribution |
| CC BY-SA | Attribution-ShareAlike 4.0 | Similar to GPL's viral nature |
| CC BY-NC | Attribution-NonCommercial 4.0 | No commercial use |
| CC BY-NC-SA | Attribution-NonCommercial-ShareAlike 4.0 | No commercial use, derivative works must use same license |
| CC BY-ND | Attribution-NoDerivatives 4.0 | No modifications allowed |
| CC BY-NC-ND | Attribution-NonCommercial-NoDerivatives 4.0 | Most restrictive |

### 8.4 CC License Usage in Open Source Projects

**Recommended CC Licenses**:
- **CC0**: For example code, test data
- **CC BY 4.0**: For documentation, tutorials
- **CC BY-SA 4.0**: For documentation that needs to remain open

**CC Licenses Not Recommended for Software**:
- CC BY-NC: Violates the "no discrimination" clause of the Open Source Definition (OSD)
- CC BY-ND: Does not allow modifications, not suitable for open source

### 8.5 License Selection for Open Source Project Documentation

```markdown
## Documentation License

This project's documentation is released under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.

You are free to:
- **Share**: Copy, distribute, and transmit this work in any medium or format
- **Adapt**: Modify, transform, and build upon this work

Under the following conditions:
- **Attribution**: You must provide appropriate attribution
```

---

## 9. License Compatibility Matrix

### 9.1 What is License Compatibility

License compatibility determines whether you can mix code with different licenses in the same project. If code under License A can be incorporated into a project under License B, we say "A is compatible with B."

### 9.2 Compatibility Matrix

The following table shows compatibility between mainstream licenses (Row → Column indicates "whether code under Row license can be placed into Column license project"):

|  | MIT | Apache 2.0 | BSD | GPLv2 | GPLv3 | AGPLv3 | LGPL | MPL 2.0 |
|--|-----|------------|-----|-------|-------|--------|------|---------|
| **MIT** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Apache 2.0** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **BSD** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **GPLv2** | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **GPLv3** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| **AGPLv3** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **LGPL** | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **MPL 2.0** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |

### 9.3 Common Compatibility Issues

**Apache 2.0 and GPLv2 Incompatibility**:
- Apache 2.0's patent authorization terms conflict with GPLv2
- Solution: Use GPLv3 (explicitly compatible)

**Mixing GPL with MIT/BSD**:
- MIT/BSD code can be placed into GPL projects
- But GPL code cannot be placed into MIT/BSD projects (due to GPL's viral nature)

**MPL 2.0 Flexibility**:
- MPL 2.0's file-level viral nature makes it compatible with many licenses
- But MPL files cannot be placed directly into pure GPL v2 projects

### 9.4 Practical Recommendations

1. **Avoid mixing strong copyleft licenses**: Such as GPL + AGPL
2. **Prefer permissive licenses**: If maximum compatibility is needed
3. **Check dependency licenses**: Use tools like `license-checker` (npm), `cargo-license` (Rust)
4. **Document license decisions**: Explain in project documentation why specific licenses were chosen

---

## 10. How to Choose an Open Source License (Decision Tree)

### 10.1 Decision Process

Choosing an open source license can follow this decision tree:

```
What do you want to open source?
│
├── Software/Code
│   │
│   ├── Do you want your code to be widely used (including closed-source projects)?
│   │   │
│   │   ├── Yes → Do you need patent protection?
│   │   │   ├── Yes → Apache License 2.0
│   │   │   └── No → MIT License
│   │   │
│   │   └── No → Do you want derivative works to also be open source?
│   │       │
│   │       ├── Yes → Do derivative works include network services?
│   │       │   ├── Yes → AGPL v3
│   │       │   └── No → GPL v3
│   │       │
│   │       └── No → Do only modified files need to be open source?
│   │           ├── Yes → MPL 2.0
│   │           └── No → LGPL v3
│   │
│   └── Are you developing a library?
│       ├── Yes → Want closed-source software to be able to link?
│       │   ├── Yes → MIT / Apache 2.0
│       │   └── No → LGPL v3
│       └── No → Refer to the above decisions
│
└── Documentation/Resources
    ├── Want completely free use → CC0
    ├── Only require attribution → CC BY 4.0
    └── Require derivative works to use same license → CC BY-SA 4.0
```

### 10.2 Quick Selection Guide

| Scenario | Recommended License | Reason |
|------|----------|------|
| Personal Tool Projects | MIT | Simple, widely accepted |
| Enterprise Open Source Projects | Apache 2.0 | Patent protection, enterprise-friendly |
| Projects Wanting to Stay Open Source | GPL v3 | Strong viral nature, patent protection |
| SaaS Projects | AGPL v3 | Prevents closed-source SaaS use |
| Open Source Libraries | MIT / Apache 2.0 | Maximizes adoption |
| Documentation Projects | CC BY 4.0 | Suitable for non-code content |
| Example Code | MIT / CC0 | Allows free use |

### 10.3 Recommendations for Chinese Developers

Based on practices in the Chinese open source community, here are recommendations:

**Startups**:
- Choose Apache 2.0 or MIT
- Avoid GPL (may limit business models)

**Individual Developers**:
- MIT is the safest choice
- If you want to protect open source nature, choose GPL v3

**Enterprise-Level Projects**:
- Apache 2.0 (with patent protection)
- Or enterprise-customized licenses

**Documentation and Tutorials**:
- CC BY 4.0 (allows reproduction, requires attribution)
- Or MIT (simple and universal)

---

## 11. Dual Licensing and Commercial Licensing

### 11.1 Dual Licensing Model

Dual Licensing refers to releasing the same software under two or more licenses, allowing users to choose the license that suits them.

**Typical Model**: GPL + Commercial License

- GPL version: Free to use, but derivative works must be open source
- Commercial license: Paid use, no need to open source derivative works

**Success Stories**:
- **MySQL**: GPL + Commercial License
- **Qt**: LGPL + Commercial License
- **MongoDB**: AGPL + Commercial License (early)
- **Redis**: BSD + Enterprise License

### 11.2 Commercial Licensing Model

Commercial License allows enterprises to obtain more permissive usage rights through payment:

**Common Models**:
- **One-Time Purchase**: One-time payment, perpetual use
- **Subscription**: Pay annually/monthly, continuous updates
- **Usage-Based Billing**: Billed based on API calls, user count, etc.
- **Enterprise Agreement**: Customized based on enterprise size and needs

### 11.3 Open Core Model

Many companies adopt the "Open Core" model:

```
Product Structure
├── Open Core (Community Edition)
│   ├── Uses open source license (e.g., Apache 2.0)
│   ├── Basic features
│   └── Community support
│
└── Commercial Extensions (Enterprise Edition)
    ├── Commercial license
    ├── Advanced features
    ├── Enterprise support
    └── SLA guarantees
```

**Success Stories**:
- **GitLab**: MIT core + Enterprise edition extensions
- **Elastic**: Apache 2.0 core + Enterprise features
- **Confluent**: Apache Kafka + Confluent Platform

### 11.4 CLA (Contributor License Agreement)

CLA (Contributor License Agreement) is a legal agreement between contributors and project maintainers that clarifies contributors' rights grants.

**Purpose of CLA**:
- Ensures the project has the right to change licenses
- Protects the project from patent litigation
- Clarifies contributors' intellectual property grants

**Common CLA Types**:
- **Individual CLA**: Signed by individual contributors
- **Corporate CLA**: Signed by companies on behalf of their employees
- **DCO** (Developer Certificate of Origin): Lightweight alternative

---

## 12. Legal Issues of Open Source Licenses

### 12.1 Legal Force of Open Source Licenses

Open source licenses are legally binding, as confirmed in multiple judicial cases:

**Jacobsen v. Katzer (2008)**: The U.S. Federal Circuit confirmed that the Artistic License is an enforceable contract.

**Cisco/FSF Settlement (2009)**: FSF sued Cisco for GPL violation, ultimately reaching a settlement.

**Oracle v. Google (2021)**: The U.S. Supreme Court ruled Google's use of Java APIs as fair use.

### 12.2 Legal Consequences of Violating Open Source Licenses

Violating open source licenses may result in:

1. **Copyright Infringement Lawsuit**: Unauthorized use of copyrighted code
2. **Contract Breach Lawsuit**: Violation of license terms
3. **Injunction**: Courts may prohibit you from continuing to use or distribute the software
4. **Damages**: You may need to compensate copyright holders for losses
5. **Reputation Loss**: Loss of credibility in the open source community

### 12.3 Open Source Licenses Under Chinese Law

Under the Chinese legal system, the legal force of open source licenses is primarily based on:

**Copyright Law**: Code is protected as a literary work

**Contract Law**: Open source licenses may constitute a contractual relationship

**Computer Software Protection Regulations**: Specifically protects intellectual property of computer software

**Judicial Practice**:
- In 2021, the Hangzhou Internet Court confirmed for the first time that GPL has legal force in China
- Multiple local courts have recognized the binding force of open source licenses

### 12.4 Compliance Audit

Steps for enterprises to conduct open source compliance audits:

1. **Identify Open Source Components**: Scan codebase to identify all open source dependencies
2. **Analyze Licenses**: Determine the open source license of each component
3. **Assess Compliance**: Check if all license requirements are met
4. **Develop Strategy**: Determine how to handle incompatible components
5. **Continuous Monitoring**: Establish ongoing compliance monitoring mechanisms

---

## 13. LICENSE File and SPDX Identifiers

### 13.1 LICENSE File Specification

Every open source project should include a `LICENSE` file in the root directory:

**File Naming**:
- `LICENSE` (recommended, GitHub will auto-detect)
- `LICENSE.md` (Markdown format)
- `LICENSE.txt` (plain text format)
- `COPYING` (GNU traditional naming)

**File Content**:
- Full license text
- Copyright notice
- Year and copyright holder

### 13.2 SPDX Identifiers

SPDX (Software Package Data Exchange) is a standard format for identifying open source licenses used in software packages.

**SPDX License Identifiers**:

| License | SPDX Identifier |
|------|-----------|
| MIT License | MIT |
| Apache License 2.0 | Apache-2.0 |
| BSD 2-Clause | BSD-2-Clause |
| BSD 3-Clause | BSD-3-Clause |
| GNU GPL v2 | GPL-2.0-only |
| GNU GPL v3 | GPL-3.0-only |
| GNU LGPL v2.1 | LGPL-2.1-only |
| GNU LGPL v3 | LGPL-3.0-only |
| GNU AGPL v3 | AGPL-3.0-only |
| Mozilla Public License 2.0 | MPL-2.0 |

### 13.3 Using SPDX Identifiers in Code

**Source File Header**:
```python
# SPDX-License-Identifier: MIT
# Copyright (c) 2024 Your Name
```

**package.json**:
```json
{
  "name": "your-package",
  "license": "MIT"
}
```

**Cargo.toml**:
```toml
[package]
name = "your-crate"
license = "MIT OR Apache-2.0"
```

**setup.py**:
```python
setup(
    name='your-package',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
)
```

### 13.4 GitHub's License Support

GitHub provides the following features to help manage open source licenses:

1. **Auto-Detection**: GitHub automatically detects LICENSE files and displays the license name
2. **License Templates**: You can select license templates when creating repositories
3. **License Comparison**: License details can be viewed on repository pages
4. **Dependabot**: Automatically detects license compliance of dependencies

---

## 14. Chinese Enterprise Open Source Compliance Guide

### 14.1 Current State of Open Source in China

China has become the world's second-largest open source contributor, but still faces challenges in open source compliance:

**Main Challenges**:
- Insufficient understanding of the legal force of open source licenses
- Incomplete enterprise compliance processes
- Lack of professional open source compliance talent
- Compliance issues with legacy code

### 14.2 Enterprise Open Source Compliance Framework

Steps to establish an enterprise open source compliance framework:

**Step 1: Establish Policies**
- Develop enterprise open source usage policies
- Clearly define allowed and prohibited open source licenses
- Establish open source approval processes

**Step 2: Form Teams**
- Establish an open source compliance committee
- Include legal, technical, and security roles
- Designate an open source compliance officer

**Step 3: Build Tools**
- Deploy open source scanning tools (such as FOSSA, Black Duck, Snyk)
- Establish an open source component database
- Integrate into CI/CD pipelines

**Step 4: Process Management**
- Compliance review before new projects go open source
- Regular compliance audits
- Employee training and awareness improvement

### 14.3 Open Source Scanning Tools

| Tool | Type | Features |
|------|------|------|
| FOSSA | Commercial | Comprehensive compliance management platform |
| Black Duck | Commercial | Enterprise-level open source risk management |
| Snyk | Commercial | Security + Compliance |
| ScanCode | Open Source | Open source license detection tool |
| FOSSology | Open Source | Open source compliance analysis tool |
| licensee | Open Source | License detection tool developed by GitHub |

### 14.4 Compliance Checklist

**Before Using Open Source Code**:
- [ ] Confirm open source license
- [ ] Assess license compatibility with project business model
- [ ] Check if source code needs to be published
- [ ] Confirm patent terms
- [ ] Document usage

**When Publishing Open Source Projects**:
- [ ] Choose appropriate open source license
- [ ] Create complete LICENSE file
- [ ] Add SPDX identifiers
- [ ] Prepare NOTICE file (if needed)
- [ ] Establish contributor agreements (CLA/DCO)

### 14.5 Best Practices for Chinese Enterprises

**Huawei**:
- Established a comprehensive open source compliance system
- Actively participates in international open source projects
- Released multiple open source projects (such as openEuler, MindSpore)

**Alibaba**:
- Established an open source committee
- Contributed to multiple top open source projects (such as Apache Flink, Apache RocketMQ)
- Established open source compliance processes

**Tencent**:
- Actively participates in the open source community
- Contributed to multiple open source projects (such as Tars, Angel)
- Established an open source governance platform

---

### 15. Common License Misconceptions

Open source licenses are one of the most important legal documents in open source projects, but many developers have misconceptions about them. Here are fifteen of the most common misconceptions to help you correctly understand the meaning and application of open source licenses.

#### Misconception 1: "Open source means free"

Many people think open source software is free software, which is a common misconception. The core of open source is the openness and sharing of source code, not the price. In fact, many open source projects achieve commercialization through various methods:

- **Commercial Licenses**: Offering paid commercial versions with additional features and support
- **Hosting Services**: Providing cloud-hosted SaaS services
- **Technical Support**: Providing paid technical support and consulting services
- **Training and Certification**: Providing paid training and certification services
- **Dual Licensing Model**: Offering both open source and commercial versions simultaneously

For example, Red Hat built a multi-billion dollar enterprise based on open source Linux distributions, primarily profiting through subscription services. Companies like MongoDB, Elastic, and Confluent have also successfully commercialized open source projects.

#### Misconception 2: "MIT License can be used freely without doing anything"

Although MIT License is permissive, it still has clear requirements. When using MIT-licensed code, you must:

1. **Retain Copyright Notice**: Retain the original copyright notice in all copies or substantial portions
2. **Retain Permission Notice**: Retain the complete MIT license notice text
3. **Include in Software**: These notices must be included in all copies of the software

This means that even if you use MIT code in closed-source commercial software, you must include the original copyright notice and license notice somewhere in the software (such as an about page, documentation, or license file).

In practice, many companies display these notices in the software's "About" dialog, LICENSE file in the installation directory, or the software's settings page.

#### Misconception 3: "GPL code cannot be used commercially"

This is a very common misconception. GPL explicitly allows commercial use. You can:

- Sell copies of GPL software
- Provide paid support services for GPL software
- Use GPL software in commercial environments
- Build business models based on GPL software

GPL does not prohibit commercial use, but requires:

1. **Open Source Derivative Works**: If you modify GPL code and distribute it, the modified version must be released under GPL
2. **Provide Source Code**: When distributing GPL software, you must also provide source code or a way to obtain it
3. **Maintain GPL**: Derivative works must use the same GPL license

Companies like Red Hat, SUSE, and Canonical have all built successful business models based on GPL software (Linux).

#### Misconception 4: "I modified open source code, so I can close source it"

This depends on the open source license you're using:

**Licenses Allowing Closed-Source Modifications**:
- MIT License
- BSD License
- Apache License 2.0
- ISC License

**Licenses Requiring Open Source Modifications**:
- GPL (all derivative works must be open source)
- AGPL (including network services)
- LGPL (only the library itself needs to be open source)
- MPL 2.0 (modified files need to be open source)

If you use GPL code and modify it, when you distribute the modified version, you must release the source code under GPL. But if you only use it internally without distribution, you are not bound by this restriction (except for AGPL).

#### Misconception 5: "If I don't publish source code, I'm not bound by open source licenses"

This misconception involves the definition of "Distribution." The meaning of distribution varies across different licenses:

**GPL v2/v3**: Distribution refers to providing copies of the software to third parties. If you only use it within your company, it generally doesn't count as distribution.

**AGPL v3**: Providing services over a network also counts as distribution. If you modify AGPL code and provide services over a network, you must provide the modified source code to all users.

**Practical Examples**:
- If you modify an AGPL web application and deploy it to a server, all users accessing that service have the right to obtain your modifications
- Many cloud service providers avoid using AGPL software because of this clause

#### Misconception 6: "Open source licenses are contracts that require signatures to be valid"

The legal force of open source licenses is interpreted differently across different legal systems:

**U.S. Law**: Open source licenses are generally treated as contracts, with acceptance of terms indicated through use of the software ("click-wrap" or "browse-wrap").

**EU Law**: Open source licenses may be treated as licenses rather than contracts, but still have legal binding force.

**Chinese Law**: Chinese courts have confirmed the legal force of GPL in multiple cases, generally treating it as a contractual relationship.

The key point is: You don't need a physical signature to accept an open source license. By copying, using, or modifying open source code, you have already accepted the license terms.

#### Misconception 7: "I can put MIT code into a GPL project, and then the entire project becomes MIT"

This understanding is incorrect. License compatibility is one-way:

- MIT code can be placed into GPL projects (because MIT allows more permissive use)
- But the entire project must comply with GPL requirements (because GPL has viral nature)

When you put MIT code into a GPL project:
1. MIT code still maintains MIT license
2. But all derivative works of the entire project must be released under GPL
3. You cannot re-release the entire project under MIT

This is why you must carefully consider compatibility issues when mixing code with different licenses.

#### Misconception 8: "Creative Commons can be used for software"

Creative Commons licenses explicitly state they are not recommended for software:

> "Creative Commons public licenses are not recommended for software. We recommend using specialized software licenses such as GNU GPL, BSD, or MIT licenses."

Reasons include:

1. **Source Code/Binary Distinction**: CC licenses do not account for the software-specific distinction between source code and binary forms
2. **Linking Issues**: CC licenses do not address software-specific issues like static and dynamic linking
3. **Installation Information**: CC licenses do not consider technical details of software installation and operation
4. **Patent Issues**: CC licenses do not have explicit patent terms

CC licenses are suitable for:
- Documentation and tutorials
- Images and multimedia resources
- Educational materials
- Datasets

#### Misconception 9: "I referenced an open source library, so my project must be open source"

This depends on how you reference the open source library and the license being used:

**Dynamic Linking**:
- Using MIT/BSD/Apache libraries: Your project can remain closed source
- Using LGPL libraries: Your project can remain closed source, but must allow users to replace the library
- Using GPL libraries: Generally requires open source (controversial)

**Static Linking**:
- Using MIT/BSD/Apache libraries: Your project can remain closed source
- Using LGPL libraries: Need to provide object files or source code
- Using GPL libraries: Generally requires open source

**Best Practices**:
- If unsure, use libraries with permissive licenses
- Consult legal counsel
- Use dependency analysis tools to check licenses

#### Misconception 10: "Open source licenses have different legal force in different countries"

Although legal systems differ across countries, open source licenses have been recognized in major jurisdictions:

**United States**: Multiple federal courts have confirmed the legal force of open source licenses, such as the Jacobsen v. Katzer case.

**European Union**: EU courts recognize the binding force of open source licenses, and German courts have supported GPL in multiple cases.

**China**: In 2021, the Hangzhou Internet Court confirmed for the first time that GPL has legal force in China. Since then, multiple local courts have made similar rulings.

**Japan**: Japanese courts have recognized the force of GPL in multiple cases.

The key point is: Open source licenses have legal force in most developed countries, and violating licenses may lead to serious legal consequences.

#### Misconception 11: "Open source code doesn't require attributing the original author"

This is a dangerous misconception. Most open source licenses require retaining the original author's attribution:

**MIT License**: Requires retaining copyright notice and permission notice

**BSD License**: Requires retaining copyright notice and disclaimer, and BSD 3-Clause also prohibits using the original author's name for endorsement

**Apache 2.0**: Requires retaining copyright notice, patent notice, trademark notice, and attribution notice

**GPL**: Requires retaining all copyright notices and permission notices

Non-compliance may result in:
- Automatic termination of license authorization
- Facing copyright infringement lawsuits
- Being required to stop using the relevant code

#### Misconception 12: "I can mix any license's code in my own project"

License compatibility is a complex issue; not all licenses can be mixed:

**Simplified Compatibility Matrix**:
- Permissive (MIT/BSD/Apache) → Can be placed in most projects
- Weak Copyleft (LGPL/MPL) → Has certain restrictions
- Strong Copyleft (GPL/AGPL) → Strict restrictions

**Common Incompatibilities**:
- Apache 2.0 is incompatible with GPL v2 (Apache's patent terms conflict with GPL v2)
- Different versions of GPL may be incompatible (GPL v2 with GPL v3)

**Recommendations**:
- Check the license of dependency libraries when selecting them
- Use license compatibility checking tools
- Consult legal experts

#### Misconception 13: "Once a license is chosen, it cannot be changed"

Actually, licenses can be changed, but specific conditions must be met:

**Condition 1: You Own All Copyrights**
- If you are the sole author of the code, you can change the license at any time
- If there are other contributors, you need to obtain consent from all contributors

**Condition 2: Use CLA**
- If the project requires contributors to sign a CLA, and the CLA allows license changes
- You can change the license based on the CLA authorization

**Condition 3: Dual Licensing**
- You can release code under multiple licenses simultaneously
- Users can choose the license that suits them

**Practical Examples**:
- MongoDB changed from AGPL to SSPL
- Elasticsearch changed from Apache 2.0 to SSPL
- WordPress plugins changed from GPL v2 to GPL v3

#### Misconception 14: "I used open source code, so I automatically received patent authorization"

This depends on the license:

**Licenses with Explicit Patent Authorization**:
- Apache License 2.0: Explicitly grants patent licenses
- GPL v3: Explicitly grants patent licenses
- MPL 2.0: Explicitly grants patent licenses

**Licenses without Explicit Patent Authorization**:
- MIT License: No explicit patent terms
- BSD License: No explicit patent terms
- GPL v2: Has implied patent authorization, but not explicit enough

If your project involves patent technology, recommendations include:
- Use licenses with explicit patent terms (such as Apache 2.0)
- Require contributors to sign CLA
- Conduct patent risk assessments

#### Misconception 15: "Open source code has no guarantees, and the original author has no responsibility if problems occur"

Most open source licenses do contain disclaimers, but this doesn't mean there is no responsibility:

**Purpose of Disclaimers**:
- Limit the original author's liability
- Explicitly state software is provided "as is"
- Exclude certain types of warranties

**Limitations of Disclaimers**:
- Cannot exclude liability for intentional fraud
- Cannot violate consumer protection laws
- May be partially invalid in certain jurisdictions

**Best Practices**:
- Conduct thorough testing before using open source code
- Understand the security and reliability of the code
- Don't use unverified open source code in critical systems
- Establish security vulnerability response mechanisms

---

## Appendix A: Open Source License Quick Reference

---

## 16. Open Source License Practical Case Studies

### 16.1 Case 1: Personal Project License Selection

Xiao Ming is a frontend developer who developed a lightweight JavaScript tool library. He hopes this library will be widely used, including by commercial companies. His choices are:

**Analysis**:
- Wants code to be widely used → Needs a permissive license
- Allows commercial use → Cannot choose licenses with non-commercial clauses
- Library nature → No viral nature needed

**Recommendation**: MIT License

**Reason**: MIT License is simple and clear with very few restrictions, making it safe for virtually all companies to use. Well-known frontend projects like React and Vue.js use MIT License, which has allowed them to be widely integrated into various commercial products.

**Practical Steps**:
```bash
# Create LICENSE file in project root
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 Xiao Ming

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
```

### 16.2 Case 2: Enterprise Open Source Project

A technology company developed a microservices framework and hopes to open source it to gain community contributions while protecting their patented technology. The company's legal department is concerned that competitors might use patent clauses to initiate lawsuits.

**Analysis**:
- Enterprise-level project → Needs patent protection
- Wants community contributions → Needs clear contributor agreements
- Concerned about patent litigation → Needs patent retaliation clause

**Recommendation**: Apache License 2.0 + CLA

**Reason**: Apache 2.0 provides explicit patent authorization and patent retaliation clauses, effectively protecting enterprise interests. Additionally, combined with CLA (Contributor License Agreement), it ensures all contributors' patents are also authorized to the project.

**Enterprise Open Source Compliance Checklist**:
1. Legal department reviews license terms
2. Establish CLA signing process
3. Scan code for third-party open source components
4. Ensure all dependency licenses are compatible
5. Clearly declare license in README
6. Establish contributor guidelines

### 16.3 Case 3: Open Source SaaS Platform

A startup developed a project management tool and provides online SaaS services. They want to keep the code open source but don't want competitors to directly take the code and deploy identical services.

**Analysis**:
- Provides network services → GPL's distribution terms don't apply
- Wants to stay open source → Needs open source license
- Prevent direct competition → Needs network use terms

**Recommendation**: AGPL v3

**Reason**: AGPL v3 closes GPL's "network use loophole," requiring projects that provide services over a network to also publish source code. This means competitors who want to use the code to provide services must also open source their modifications.

**Considerations**:
- AGPL's viral nature is strong and may deter some enterprise users
- Need to clearly inform users of their obligations
- Consider providing commercial license options

### 16.4 Case 4: Commercialization of Open Source Libraries

A popular open source library maintainer wants to profit from the project while maintaining the open source nature of the code.

**Analysis**:
- Wants to profit → Needs commercial license model
- Maintain open source → Needs open core
- Library nature → Need to consider user scenarios

**Recommendation**: LGPL v3 (library) + Commercial License

**Model Design**:
```
Project Structure
├── Core Library (LGPL v3)
│   ├── Basic Features
│   └── Open source, allows closed-source linking
│
├── Extension Plugins (Commercial License)
│   ├── Advanced Features
│   └── Paid usage
│
└── Enterprise Edition (Commercial License)
    ├── Complete Features
    ├── Technical Support
    └── SLA Guarantees
```

**Success Story References**:
- Qt: LGPL + Commercial License
- MySQL: GPL + Commercial License
- Redis: BSD + Enterprise License

### 16.5 Case 5: Academic Project Open Sourcing

A university research team developed a machine learning algorithm library and hopes both academia and industry can use it while ensuring academic citations.

**Analysis**:
- Academic project → Needs citation requirements
- Industry use → Needs permissive license
- Machine learning field → Apache 2.0 is common

**Recommendation**: Apache License 2.0 + Citation File

**Implementation Method**:
```markdown
## Citation

If this project is helpful to your research, please cite our paper:

```bibtex
@article{author2024paper,
  title={Paper Title},
  author={Author Name},
  journal={Journal Name},
  year={2024}
}
```
```

### 16.6 License Migration Case Study

**Case: MongoDB License Change**

MongoDB changed its license from AGPL v3 to SSPL (Server Side Public License) in 2018, sparking widespread discussion.

**Reasons for Change**:
- Cloud service providers directly using MongoDB to provide hosted services
- Original license did not effectively protect MongoDB's commercial interests

**Impact of Change**:
- Some open source organizations did not recognize SSPL
- Some Linux distributions removed MongoDB
- Spawned compatible projects like FerretDB

**Lessons**:
- License changes need careful consideration
- Assess community and user reactions in advance
- Prepare response plans

### 16.7 Multi-License Project Management

Large projects may contain code under multiple licenses and need systematic management:

**Directory Structure Example**:
```
project/
├── src/
│   ├── core/           # Core code, Apache 2.0
│   ├── plugins/
│   │   ├── plugin-a/   # Plugin A, MIT
│   │   └── plugin-b/   # Plugin B, BSD 3-Clause
│   └── third-party/
│       ├── lib-x/      # Third-party library X, LGPL
│       └── lib-y/      # Third-party library Y, Apache 2.0
├── docs/               # Documentation, CC BY 4.0
├── examples/           # Example code, MIT
└── LICENSE             # Main project license
```

**License Management Tools**:
```bash
# npm projects
npm install -g license-checker
license-checker --summary

# Python projects
pip install pip-licenses
pip-licenses --format=table

# Rust projects
cargo install cargo-license
cargo license
```

---

## Appendix A: Open Source License Quick Reference

| License | Viral Nature | Patent Protection | Trademark Protection | Recommended Scenario |
|------|--------|----------|----------|----------|
| MIT | None | None | None | General projects |
| Apache 2.0 | None | Yes | Yes | Enterprise projects |
| BSD 2-Clause | None | None | None | MIT-like |
| BSD 3-Clause | None | None | Yes | Attribution protection needed |
| GPL v2 | Strong | Implied | None | Linux kernel |
| GPL v3 | Strong | Yes | None | General GPL projects |
| AGPL v3 | Strong (includes network) | Yes | None | SaaS projects |
| LGPL v3 | Weak (library) | Yes | None | Open source libraries |
| MPL 2.0 | File-level | Yes | None | Mixed projects |
| CC BY 4.0 | None | None | None | Documentation |
| CC BY-SA 4.0 | Yes | None | None | Documentation that needs to stay open |
| CC0 | None | None | None | Public domain |

## Appendix B: Recommended Reading

- [Open Source Initiative (OSI)](https://opensource.org/)
- [Free Software Foundation (FSF)](https://www.fsf.org/)
- [SPDX License List](https://spdx.org/licenses/)
- [Choose a License](https://choosealicense.com/)
- [TLDRLegal](https://tldrlegal.com/)
- [China Open Source Cloud League](http://www.coscl.org.cn/)
- [OpenAtom Foundation](https://www.openatom.org/)

---

**Last Updated**: December 2024

**Disclaimer**: This document is for learning reference only and does not constitute legal advice. When making important open source license decisions, please consult professional legal counsel.