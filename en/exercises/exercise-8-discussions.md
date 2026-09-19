# Exercise 8: Setting Up GitHub Discussions

## Goal

Learn how to set up and manage GitHub Discussions.

## Steps

### 1. Create a Practice Repository

```bash
mkdir discussions-practice
cd discussions-practice
git init

echo "# Discussions Practice" > README.md
git add README.md
git commit -m "Initial commit"

git remote add origin git@github.com:your-username/discussions-practice.git
git push -u origin main
```

### 2. Enable Discussions

1. Go to the repository **Settings**
2. In the **Features** section, check **Discussions**
3. Click **Set up discussions**

### 3. Configure Categories

1. Go to the **Discussions** tab
2. Click **Categories**
3. Review the default categories:

| Category | Icon | Purpose |
|----------|------|---------|
| Announcements | 📣 | Official announcements |
| General | 💬 | General discussions |
| Ideas | 💡 | Ideas and suggestions |
| Q&A | 🙋 | Questions and answers |
| Show and tell | 📝 | Showcase and share |

### 4. Create a Custom Category

1. Click **New category**
2. Fill in the details:
   - **Name**: Resources
   - **Description**: Share useful resources and links
   - **Emoji**: 📚
   - **Discussion format**: Open-ended discussion
3. Click **Create**

### 5. Create Your First Discussion

#### Create an Announcement

1. Click the **Announcements** category
2. Click **New discussion**
3. Enter the title: `Welcome to our community!`
4. Enter the content:

```markdown
# Welcome!

Welcome to our Discussions community.

## Community Guidelines

1. Respect others
2. Be friendly
3. Share valuable content

## How to Participate

- Ask questions in **Q&A**
- Share ideas in **Ideas**
- Showcase your work in **Show and tell**

Looking forward to your participation! 🎉
```

5. Click **Start discussion**

### 6. Create a Q&A

1. Click the **Q&A** category
2. Click **New discussion**
3. Enter the title: `How to configure the project?`
4. Enter the content:

```markdown
# Question

I am encountering the following issues when configuring the project...

## Methods Already Tried

1. Method 1
2. Method 2

## Expected Results

Looking for guidance on the configuration.
```

### 7. Answer the Question

1. Open the Q&A you just created
2. Enter your answer in the comment box:

```markdown
# Solution

You can follow these steps to configure:

1. Step one
2. Step two
3. Step three

Hope this helps!
```

3. Click **Comment**

### 8. Mark the Best Answer

1. Click the **...** menu on the answer
2. Select **Mark as answer**

The best answer will be highlighted.

### 9. Create an Ideas Discussion

1. Click the **Ideas** category
2. Click **New discussion**
3. Enter the title: `Suggestion: Add dark mode`
4. Enter the content:

```markdown
# Feature Suggestion

## Description

Suggest adding dark mode support to improve user experience.

## Motivation

- Protect users' eyes
- Align with modern UI trends
- Improve accessibility

## Implementation Plan

Use CSS variables and JavaScript to toggle themes.

## Screenshots

(Add design mockups here if available)

What does everyone think? 👍 or 👎
```

### 10. Use Labels

1. On the right side of the Discussion, click **Labels**
2. Add labels: `enhancement`, `community`

### 11. Convert to an Issue

If a discussion turns out to be a bug:
1. Click **Convert to issue**
2. Fill in the Issue details
3. Click **Create issue**

### 12. Lock a Discussion

If a discussion is resolved:
1. Click **Lock discussion**
2. Select a reason for locking
3. Click **Lock this discussion**

## Management Best Practices

### Category Management

1. **Regular cleanup**: Remove meaningless content
2. **Merge similar discussions**: Avoid duplicates
3. **Update categories**: Adjust as needed

### Community Management

1. **Respond promptly**: Keep the community active
2. **Mark answers**: Help future visitors
3. **Encourage participation**: Thank contributors
4. **Set rules**: Maintain discussion order

## Key Takeaways

- Enabling Discussions
- Configuring categories
- Creating and managing discussions
- Q&A best answers
- Using labels
- Converting discussions
- Locking discussions

## Related Resources

- [GitHub Discussions Official Documentation](https://docs.github.com/en/discussions)
- [Using Discussions for Community Management](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions)
