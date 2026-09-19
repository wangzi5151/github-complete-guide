# GitHub Projects Complete Project Management Guide

> GitHub Projects is GitHub's official project management tool, helping development teams plan, track and manage software development work. This article will deeply introduce various features of GitHub Projects, from basic configuration to advanced usage, helping you efficiently manage projects.

---

## 1. GitHub Projects Overview

### New Projects vs Classic Projects

GitHub launched the new Projects (also called Projects V2) in 2022, with a qualitative leap compared to the classic version.

| Feature | Classic Projects | New Projects (V2) |
|---------|-----------------|-------------------|
| View Types | Only board view | Board, Table, Roadmap |
| Custom Fields | Limited support | Full support for multiple field types |
| Automation | Basic rules | Powerful built-in automation |
| Data Analysis | None | Built-in charts and reports |
| Cross-repo Support | Not supported | Fully supported |
| Iteration Management | Not supported | Built-in iteration cycles |
| API Support | REST API | GraphQL API |

**Core Advantages of New Projects:**

- **Flexible View System**: Same project data can be presented in board, table, roadmap and other ways
- **Rich Custom Fields**: Support single select, multi select, date, number, iteration and other field types
- **Powerful Automation**: Multiple built-in automation rules, reducing manual operations
- **Deep Integration**: Seamless integration with Issues, Pull Requests, GitHub Actions
- **Real-time Collaboration**: Multiple people can edit simultaneously with real-time sync updates

### Applicable Scenarios

- **Agile Development Teams**: Manage Sprints, user stories and tasks
- **Open Source Projects**: Track Issues, PRs and release plans
- **Personal Projects**: Manage to-do items and learning plans
- **Product Management**: Plan product roadmap and version releases

### Core Concepts of GitHub Projects

Before deep learning, need to understand the following core concepts:

**Project**: A project is a container for organizing and managing a group of related work items. Projects can belong to personal accounts, organizations or repositories. Each project has independent field definitions, view configurations and automation rules.

**Item**: Item is the basic unit in projects, can be Issue, Pull Request or draft entry. Each item can have custom field values for recording status, priority, assignee and other information.

**View**: View is the display method of project data. Same project can create multiple views, each view can have different filter conditions, grouping methods, sorting rules and display formats.

**Field**: Field defines item attributes. GitHub Projects provides preset fields (like Status, Assignees, Labels), also supports creating custom fields to meet specific needs.

**Workflow**: Workflow is a collection of automation rules, used to automatically execute operations when specific events occur, for example when Issue is added to project, automatically set status to "To Do".

---

## 2. Create and Configure Project Board

### Create via Web Interface

**Step 1: Enter Project Creation Page**

1. Open GitHub repository page
2. Click **Projects** tab at top
3. Click green **New project** button

**Step 2: Select Project Type**

GitHub provides multiple project templates:

- **Board**: Board view, suitable for task workflow management
- **Table**: Table view, suitable for data analysis
- **Roadmap**: Roadmap view, suitable for time planning

**Step 3: Configure Project Basic Information**

```
Project Name: My Awesome Project
Project Description: Manage project development progress and task assignment
README: Optional, add project description
```

**Step 4: Set Project Visibility**

- **Private**: Only visible to project members
- **Public**: Visible to everyone (suitable for open source projects)

### Create via Command Line

Using GitHub CLI can quickly create projects:

```bash
# Create personal project
gh project create --title "My Project" --owner @me

# Create organization project
gh project create --title "Team Project" --owner my-org

# Create using template
gh project create --title "Sprint 1" --owner @me --template "feature-tracker"

# View project list
gh project list --owner @me
```

### Basic Project Configuration

After creating project, recommend performing the following configurations:

**1. Set Project Fields**

After entering project, click **+** in top right corner to add custom fields. Recommend creating the following basic fields:

| Field Name | Type | Description |
|------------|------|-------------|
| Status | Single select | Task status (To Do, In Progress, Done) |
| Priority | Single select | Priority (Urgent, High, Medium, Low) |
| Assignees | People | Assignee |
| Labels | Labels | Label classification |
| Start Date | Date | Start date |
| Due Date | Date | Due date |

**2. Configure Workflow**

Click **Workflows** button to set automation rules. Recommend enabling the following basic rules:

- When Issue is added to project, automatically set Status to "To Do"
- When Issue is closed, automatically set Status to "Done"
- When PR is merged, automatically set Status to "Done"

**3. Add Project Members**

Invite team members and set permissions in project settings. GitHub Projects supports three permission levels:

- **Admin**: Full control of project settings and content
- **Write**: Can edit project items and views
- **Read**: Can only view project content

**4. Set Project Description and README**

Clear project description helps team members understand project goals. README supports Markdown format, can include:

- Project goals and scope description
- Team members and role assignments
- Workflow and specification description
- Related documentation and resource links

**5. Create Initial Views**

Create commonly used views based on team needs:

- **Board View**: For daily task management and stand-ups
- **Table View**: For data analysis and batch operations
- **Roadmap View**: For long-term planning and milestone tracking

---

## 3. Project Views

GitHub Projects provides three core views, each view is suitable for different scenarios.

### Table View

Table view provides spreadsheet-like data display, suitable for data analysis and batch operations.

**Main Features:**

- **Column Management**: Customize which field columns to display
- **Sorting Function**: Sort by any field
- **Filter Function**: Filter project items by conditions
- **Grouping Function**: Group display by field

**Use Cases:**

- View all tasks' priority and status
- Assign tasks by assignee
- Analyze project progress data

**Configuration Example:**

```
Column Display: Title, Status, Priority, Assignee, Due Date
Sort: Priority (Descending)
Group: Status
Filter: Assignee = @me
```

**Advanced Features of Table View:**

- **Column Width Adjustment**: Drag column border to adjust width, double-click to auto-fit content
- **Inline Editing**: Directly click cell to edit field value, no need to open detail panel
- **Batch Selection**: Hold Shift or Ctrl to multi-select rows, batch modify field values
- **Export Data**: Export table data to CSV format for offline analysis
- **Column Sorting**: Click column title for ascending or descending sorting

**Common Table View Configuration Schemes:**

| Configuration | Recommended Setting | Applicable Scenario |
|--------------|---------------------|---------------------|
| Column Display | Title, Status, Priority, Assignee, Sprint, Story Points | Sprint Management |
| Group | Status | Task status overview |
| Filter | -status:done | View incomplete tasks |
| Sort | Priority (Descending) | Priority first |

### Board View

Board view displays tasks in card format, update task status by dragging cards.

**Core Concepts:**

- **Columns**: Represent different work statuses
- **Cards**: Represent specific tasks or work items
- **WIP Limit**: Limit card count per column (optional)

**Default Column Configuration:**

```
To Do → In Progress → In Review → Done
```

**Custom Columns:**

You can customize columns based on team workflow:

```
Backlog → Ready → Development → Testing → Staging → Production
```

**Board Best Practices:**

- Limit Work In Progress (WIP Limit)
- Regularly clean up completed tasks
- Use labels to distinguish task types

**Card Information in Board View:**

Each card can display the following information, helping team members quickly understand task overview:

- **Title**: Brief task description
- **Status Label**: Current work stage
- **Priority Indicator**: Use colors to distinguish priority levels
- **Assignee Avatar**: Which team member assigned to
- **Due Date**: Task due time
- **Labels**: Classification labels, like Bug, Feature etc.
- **Linked PR**: Number of associated Pull Requests

**Column Configuration Details:**

Each column in board corresponds to an option of Status field. You can customize column order, color and display rules:

| Column Name | Color Suggestion | Description |
|-------------|------------------|-------------|
| Backlog | Grey | Task pool pending planning |
| To Do | Blue | Tasks to start in this iteration |
| In Progress | Yellow | Tasks in progress |
| In Review | Purple | Tasks waiting for code review |
| Done | Green | Completed tasks |

**Drag Operations:**

Board view supports intuitive drag operations:

- **Horizontal Drag**: Drag card from one column to another, automatically updates Status field
- **Vertical Drag**: Adjust card order within same column
- **Batch Drag**: Select multiple cards and drag together (some versions support)

### Roadmap View

Roadmap view displays project plans in timeline format, suitable for long-term planning and milestone management.

**Main Features:**

- **Timeline**: Display by week, month, quarter
- **Date Fields**: Use date fields to determine time range
- **Dependencies**: Visualize task dependencies
- **Milestones**: Mark important project nodes

**Use Cases:**

- Product version release planning
- Quarterly goals and key results tracking
- Cross-team coordination and dependency management

**Configuration Steps:**

1. Create date fields (like Start Date, End Date)
2. Switch to roadmap view
3. Select date fields as time range
4. Set time granularity (week/month/quarter)

**Time Granularity Selection for Roadmap View:**

| Time Granularity | Applicable Scenario | Typical Span |
|-----------------|---------------------|--------------|
| Week | Sprint planning, short-term tasks | 2-8 weeks |
| Month | Quarterly planning, version release | 1-6 months |
| Quarter | Annual planning, long-term goals | 1-4 quarters |

**Tips for Using Roadmap View:**

- **Set Milestones**: Mark important project nodes on roadmap, like version release dates, review meetings etc.
- **Color Coding**: Use different colors to distinguish task types or priorities, for quick identification
- **Zoom Operations**: Through zoom control to adjust time range display granularity, view overall or details
- **Filter Display**: Filter by assignee, priority and other conditions, only show related tasks
- **Export Share**: Screenshot or export roadmap, for meeting presentations and reports

---

## 4. Custom Fields

Custom fields are one of GitHub Projects' core features, letting you flexibly define and track project data.

### Field Type Details

#### Single Select Field

Single select field allows selecting one value from predefined options.

**Common Usage:**

```yaml
Field Name: Priority
Options:
  - Urgent: Red
  - High: Orange
  - Medium: Yellow
  - Low: Green
```

```yaml
Field Name: Category
Options:
  - Feature: Blue
  - Bug: Red
  - Enhancement: Purple
  - Documentation: Grey
```

**Configuration Steps:**

1. Click **+** in project
2. Select **Single select**
3. Enter field name
4. Add options and set colors
5. Set default value (optional)

#### Multi Select Field

Multi select field allows selecting multiple values, suitable for marking work items with multiple attributes.

**Common Usage:**

```yaml
Field Name: Tags
Options:
  - Frontend
  - Backend
  - Database
  - API
  - UI/UX
```

```yaml
Field Name: Platforms
Options:
  - iOS
  - Android
  - Web
  - Desktop
```

#### Date Field

Date field is used to set due dates or time ranges.

**Common Usage:**

- **Due Date**: Task due date
- **Start Date**: Task start date
- **End Date**: Task end date

**Application in Roadmap View:**

Roadmap view needs at least one date field to determine time range. Recommend creating two date fields:

- Start Date: Start date
- End Date: End date

#### Number Field

Number field is used to store numerical data.

**Common Usage:**

```yaml
Field Name: Story Points
Range: 1, 2, 3, 5, 8, 13, 21
Purpose: Estimate workload

Field Name: Estimated Hours
Range: 0.5, 1, 2, 4, 8, 16
Purpose: Time estimation

Field Name: Business Value
Range: 1-10
Purpose: Priority sorting
```

#### Iteration Field

Iteration field is used to manage Sprint or iteration cycles.

**Configuration Options:**

```yaml
Field Name: Sprint
Iteration Period: 2 weeks
Start Date: 2024-01-01
Iteration Count: Auto-create
Options:
  - Sprint 1 (2024-01-01 ~ 2024-01-14)
  - Sprint 2 (2024-01-15 ~ 2024-01-28)
  - Sprint 3 (2024-01-29 ~ 2024-02-11)
  - ...
```

**Special Behavior of Iteration Field:**

- Supports **Current iteration** auto-filter
- Supports **Past iterations** review
- Supports **Future iterations** planning

#### Labels Field

GitHub Labels can be directly used in projects for classification and filtering.

**Label Design Suggestions:**

```yaml
Type Labels:
  - type:bug
  - type:feature
  - type:enhancement
  - type:docs

Priority Labels:
  - priority:critical
  - priority:high
  - priority:medium
  - priority:low

Status Labels:
  - status:blocked
  - status:needs-review
  - status:ready-to-deploy
```

### Field Management Best Practices

1. **Keep Fields Concise**: Only create necessary fields, avoid information overload
2. **Unified Naming Convention**: Use consistent field naming within team
3. **Reasonable Color Usage**: Set meaningful colors for options
4. **Set Default Values**: Set default values for commonly used fields, reduce manual input
5. **Regular Cleanup**: Delete unused fields and options

### Other Field Types

#### Text Field

Text field is used to store free-form short text information. Unlike Issue or PR body, text field is suitable for recording brief supplementary information, such as notes, links or reference numbers.

**Common Usage:**

- **Notes**: Record special situations or additional explanations
- **External Links**: Associate links to external systems or documents
- **Tracking Numbers**: External system ticket numbers or requirement numbers

#### People Field

People field is used to specify people related to work items. Unlike Assignees field, custom people field can record multiple role assignees.

**Common Usage:**

- **Reviewer**: Code reviewer
- **QA Owner**: Test person in charge
- **Stakeholder**: Stakeholder or demand side

#### Field Usage Scenario Comparison Table

| Scenario | Recommended Field Type | Example |
|----------|----------------------|---------|
| Task Status Tracking | Single select | Status: To Do, In Progress, Done |
| Priority Management | Single select | Priority: Urgent, High, Medium, Low |
| Workload Estimation | Number | Story Points: 1, 2, 3, 5, 8 |
| Time Planning | Date | Due Date, Start Date |
| Iteration Management | Iteration | Sprint: Two-week cycle |
| Multi-dimensional Classification | Multi select | Tags: Frontend, Backend, Database |
| Role Assignment | People | Reviewer, QA Owner |

---

## 5. Automation Workflow

GitHub Projects provides built-in automation features, helping reduce manual operations and improve work efficiency.

### Built-in Automation Rules

#### Status Auto-update

```yaml
Rule 1: Issue added to project
Trigger: Issue is added to project
Action: Set Status to "To Do"

Rule 2: Issue closed
Trigger: Issue is closed
Action: Set Status to "Done"

Rule 3: PR created
Trigger: Pull Request is added to project
Action: Set Status to "In Progress"

Rule 4: PR merged
Trigger: Pull Request is merged
Action: Set Status to "Done"
```

#### Date Auto-set

```yaml
Rule: Set start date
Trigger: Status changes to "In Progress"
Action: Set Start Date to current date

Rule: Set completion date
Trigger: Status changes to "Done"
Action: Set End Date to current date
```

#### Cleanup Rules

```yaml
Rule: Archive completed items
Trigger: Status is "Done" and more than 14 days
Action: Archive that project item
```

### Configure Automation Rules

**Step 1: Enter Workflow Settings**

1. Open project page
2. Click **...** menu in top right corner
3. Select **Workflows**

**Step 2: Select or Create Rules**

GitHub provides preset automation templates, you can also create custom rules.

**Step 3: Configure Trigger Conditions and Actions**

```
Trigger: When issues are added to this project
Action: Set status to "To Do"
```

**Step 4: Enable Rules**

Click **Save** to save and enable rules.

### Automation Triggers and Actions Details

**Available Triggers:**

| Trigger | Description | Typical Usage |
|---------|-------------|---------------|
| Item added to project | Work item is added to project | Auto-set initial status |
| Item removed from project | Work item is removed from project | Clean up associated data |
| Issue opened | Issue is created | Add to project and classify |
| Issue closed | Issue is closed | Update status to completed |
| Pull request opened | PR is created | Mark as in progress |
| Pull request merged | PR is merged | Update status to completed |
| Label added | Label is added | Update priority by label |
| Review submitted | Code review completed | Update review status |

**Available Actions:**

| Action | Description | Typical Usage |
|--------|-------------|---------------|
| Set status | Set Status field value | Update task status |
| Set priority | Set Priority field value | Set priority by label |
| Set iteration | Set Sprint field value | Assign to current iteration |
| Set date field | Set date field value | Record start or completion time |
| Archive item | Archive work item | Clean up completed tasks |

### Custom Automation (Using GitHub Actions)

For more complex automation needs, can use GitHub Actions:

```yaml
# .github/workflows/project-automation.yml
name: Project Automation

on:
  issues:
    types: [opened, closed, reopened]
  pull_request:
    types: [opened, closed, merged]

jobs:
  update-project:
    runs-on: ubuntu-latest
    steps:
      - name: Add issue to project
        if: github.event_name == 'issues' && github.event.action == 'opened'
        uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/users/my-org/projects/1
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Update status to Done
        if: github.event_name == 'issues' && github.event.action == 'closed'
        uses: actions/update-project-item@v1
        with:
          project-url: https://github.com/users/my-org/projects/1
          item-id: ${{ steps.get-item.outputs.item-id }}
          status: "Done"
```

### Automation Workflow Best Practices

1. **Start Simple**: First use built-in rules, gradually expand
2. **Test Rules**: Test automation behavior before the official project
3. **Document**: Record automation rules' logic and purpose
4. **Regular Review**: Check if automation works as expected
5. **Avoid Over-automation**: Some manual operations may be more flexible

---

## 6. Integration with Issues and Pull Requests

GitHub Projects deeply integrates with Issues and Pull Requests, achieving seamless connection between code development and project management.

### Add Issue to Project

#### Manual Add

1. Open Issue page
2. Find **Projects** section in right sidebar
3. Click **Add to project**
4. Select target project

#### Batch Add

Batch add in project view:

1. Click **+ Add item**
2. Select **Add items from repository**
3. Select repository
4. Check Issues to add

#### Auto-add Using Labels

Configure automation rules, when Issue is labeled with specific label, automatically add to project:

```yaml
Trigger: Issue is labeled "sprint-ready"
Action: Add to project and set Status to "To Do"
```

### Add Pull Request to Project

#### Association Methods

Pull Request can be associated to project through the following methods:

1. **Manual Add**: Add in PR page's Projects section
2. **Auto Add**: When PR's associated Issue is in project, automatically add
3. **Label Trigger**: Use label auto-add rules

#### PR and Issue Linkage

When Pull Request is associated with Issue:

- PR status changes automatically update associated Issue status
- Merging PR can automatically close associated Issue
- Project status can automatically sync

**Ways to Associate Issue in PR:**

Using specific keywords in PR description can automatically associate and close Issue:

```markdown
Closes #123
Fixes #456
Resolves #789
```

Can also associate Issues from other repositories:

```markdown
Closes org/other-repo#100
```

When PR is merged, associated Issues will automatically close, if these Issues are already in project, project status will also automatically update.

**Cross-reference Tracking:**

GitHub automatically tracks reference relationships between Issues and PRs:

- Issue page will show associated PRs
- PR page will show associated Issues
- Project work items will show linked PR count

### Draft Items

GitHub Projects supports creating draft items, these entries are not yet associated with Issues or PRs.

**Use Cases:**

- Quickly record ideas, create Issue later
- Task breakdown during planning phase
- Non-code related task management

**Create Draft:**

1. Click **+ Add item** in project
2. Enter title
3. Press Enter to create draft

**Convert to Issue:**

1. Click draft item
2. Click **Create issue**
3. Select target repository
4. Fill in Issue details

### Field Sync

Some fields can sync between project and Issue/PR:

| Project Field | Issue/PR Field | Sync Direction |
|--------------|----------------|----------------|
| Status | Issue status | Bidirectional |
| Labels | Issue labels | Bidirectional |
| Assignees | Issue assignees | Bidirectional |
| Milestone | Issue milestone | One-way (from Issue to project) |
| Linked PRs | Associated PRs | Automatic |

---

## 7. Iteration (Sprint) Management

GitHub Projects' iteration field provides complete Sprint management capabilities for agile development teams.

### Configure Iteration Field

**Create Iteration Field:**

1. Add new field in project
2. Select **Iteration** type
3. Configure iteration parameters:

```yaml
Field Name: Sprint
Iteration Period: 2 weeks
Start Date: 2024-01-01 (Monday)
Iteration Count: 12 (Auto-create 12 iterations)
```

**Iteration Naming Rules:**

- Sprint 1, Sprint 2, Sprint 3...
- Or custom: Week 1-2, Week 3-4...

### Sprint Planning

**Planning Process:**

1. **Create Board View**: Group by Sprint
2. **Evaluate Workload**: Use Story Points field
3. **Assign Tasks**: Set Assignee field
4. **Set Priority**: Use Priority field

**Sprint Board Configuration:**

```
View Name: Sprint Board
Group: Sprint
Filter: Sprint = Current iteration
Sort: Priority (Descending)
```

**Sprint Planning Meeting Key Points:**

Sprint planning meeting is a key part of agile development, usually held at the beginning of each Sprint. Using GitHub Projects can make planning meetings more efficient:

1. **Review Product Backlog**: Use table view to view tasks in Backlog, sort by priority
2. **Evaluate Team Capacity**: View team members' current task assignments
3. **Select This Sprint Tasks**: Assign selected tasks to current Sprint
4. **Estimate Workload**: Assign Story Points to each task
5. **Confirm Sprint Goals**: Clarify core goals to complete in this Sprint

**Sprint Capacity Planning Suggestions:**

| Team Size | Recommended Sprint Capacity | Description |
|-----------|----------------------------|-------------|
| 3-5 people | 20-40 Story Points | Small team, fast iteration |
| 5-8 people | 40-80 Story Points | Medium team, balanced rhythm |
| 8-12 people | 80-120 Story Points | Large team, needs more coordination |

### Sprint Execution

**Daily Stand-up:**

Use board view to display current Sprint progress:

1. **To Do**: Tasks to start
2. **In Progress**: Tasks in progress
3. **In Review**: Tasks waiting for review
4. **Done**: Completed tasks

**Stand-up Flow Suggestions:**

Daily stand-up is an important meeting for team sync, recommend controlling within 15 minutes. Using GitHub Projects' board view can make stand-ups more efficient:

1. **Open Board View**: Filter current Sprint tasks
2. **Update One by One**: Each member shares yesterday's completed tasks, today's plans and encountered blockers
3. **Identify Blocks**: Focus on tasks in In Review column that have not been processed for a long time
4. **Update Status**: Directly drag to update task status on board during meeting

**Progress Tracking:**

Use table view to analyze Sprint progress:

```
Filter: Sprint = Current iteration
Group: Status
Display Fields: Title, Assignee, Story Points, Priority
```

**Sprint Progress Monitoring Metrics:**

During Sprint execution, need to focus on the following metrics to judge project health:

| Metric | Calculation | Healthy Range |
|--------|-------------|---------------|
| Completed Story Points | Sum of completed Story Points | Close to Sprint plan amount |
| Remaining Story Points | Sum of uncompleted Story Points | Decrease over time |
| Task Distribution | Task count per status | Should not concentrate in one column |
| Blocked Task Count | Tasks marked as Blocked | Fewer is better |

### Sprint Review

**Create Review View:**

```
View Name: Sprint Review
Filter: Sprint = Past iteration (most recently completed iteration)
Group: Status
Display Fields: Title, Assignee, Story Points, Actual Hours
```

**Review Metrics:**

- **Completion Rate**: Completed story points / Planned story points
- **Velocity**: Story points completed per Sprint
- **Defect Rate**: Bug count / Total task count

**Sprint Review Meeting Flow:**

Sprint review meeting is an important part for team reflection and improvement, usually held at the end of each Sprint:

1. **Data Review**: Use project charts to display Sprint completion status
2. **What Went Well**: Discuss aspects where team performed well in this Sprint
3. **What Needs Improvement**: Identify work processes or collaboration methods that can be improved
4. **Action Plan**: Formulate specific improvement measures, assign to next Sprint

**Velocity Trend Analysis:**

By tracking velocity data across multiple Sprints, can predict team delivery capacity:

```
Sprint 1: 35 Story Points
Sprint 2: 42 Story Points
Sprint 3: 38 Story Points
Sprint 4: 40 Story Points
Average Velocity: 38.75 Story Points
```

Based on average velocity, team can more accurately plan task volume for subsequent Sprints.

### Multi-team Sprint Management

For multiple teams situation, can:

1. **Use Labels to Distinguish Teams**: Team-A, Team-B
2. **Create Team Views**: Each team has a filtered view
3. **Share Iteration Fields**: Unified Sprint cycle
4. **Independent Boards**: Each team has independent board view

---

## 8. Project Filtering and Grouping

### Filter Function

Filter is an important function for quickly locating specific work items in project management.

#### Filter Syntax

```yaml
# Basic filter
status:todo
status:"in progress"
priority:high
assignee:@me

# Combined filter (AND)
status:todo priority:high
assignee:@me status:"in progress"

# Combined filter (OR)
status:todo OR status:"in progress"
priority:high OR priority:urgent

# Exclude filter
-status:done
-assignee:@me

# Date filter
due:<2024-01-31
due:>2024-01-01
due:this-week
due:this-month
start:<2024-01-15

# Iteration filter
sprint:"current iteration"
sprint:"past iteration"
sprint:"Sprint 1"

# Label filter
label:bug
label:"type:feature"
-label:"priority:low"

# Text search
Search term (search title and description)
```

#### Common Filter Combinations

**My Tasks:**
```
assignee:@me -status:done
```

**Due This Week:**
```
due:this-week assignee:@me
```

**High Priority Bugs:**
```
label:bug priority:high OR priority:urgent
```

**Current Sprint Tasks:**
```
sprint:"current iteration" -status:done
```

**Needs Review:**
```
status:"in review"
```

### Grouping Function

Grouping function classifies and displays project items by specific field.

#### Grouping Options

| Field | Description | Applicable Views |
|-------|-------------|------------------|
| Status | Group by status | All views |
| Priority | Group by priority | Table, Board |
| Assignees | Group by assignee | Table, Board |
| Labels | Group by label | Table, Board |
| Sprint | Group by iteration | Table, Board |
| Repository | Group by repository | Table, Board |
| Milestone | Group by milestone | Table, Board |
| Custom Field | Group by custom field | Table, Board |

#### Grouping Best Practices

1. **Board View**: Usually group by Status
2. **Task Assignment**: Group by Assignees to view each person's workload
3. **Priority Management**: Group by Priority to identify urgent tasks
4. **Iteration Planning**: Group by Sprint for iteration planning
5. **Cross-repo Projects**: Group by Repository to view each repository's progress

### Sort Function

Sort function helps you display project items in specific order.

#### Sort Options

```yaml
# Single field sort
Priority (Descending)  # High priority first
Due Date (Ascending)   # Earliest due first
Story Points (Descending)  # Largest workload first

# Multi-field sort
1. Priority (Descending)
2. Due Date (Ascending)
# First by priority, if same priority then by due date
```

### View Combination Application

Through combining filters, grouping and sorting, create powerful views:

**View 1: My Tasks This Week**
```
Filter: assignee:@me due:this-week -status:done
Group: Priority
Sort: Due Date (Ascending)
```

**View 2: Sprint Progress**
```
Filter: sprint:"current iteration"
Group: Status
Sort: Priority (Descending)
```

**View 3: Team Work Assignment**
```
Filter: -status:done
Group: Assignees
Sort: Priority (Descending)
```

**View 4: Bug Tracking**
```
Filter: label:bug -status:done
Group: Priority
Sort: Due Date (Ascending)
```

---

## 9. Project Templates

GitHub Projects provides multiple preset templates to help quickly start project management.

### Built-in Templates

#### Feature Tracker Template

```yaml
Fields:
  - Status: Backlog, Ready, In Progress, In Review, Done
  - Priority: Urgent, High, Medium, Low
  - Size: XS, S, M, L, XL

Views:
  - Feature Board (Board View)
  - Feature Table (Table View)
```

#### Bug Tracker Template

```yaml
Fields:
  - Status: New, Confirmed, In Progress, Verified, Closed
  - Severity: Critical, High, Medium, Low
  - Environment: Production, Staging, Development

Views:
  - Bug Board (Board View)
  - Bug Table (Table View)
```

#### Roadmap Template

```yaml
Fields:
  - Status: Planning, In Progress, Complete
  - Priority: High, Medium, Low
  - Start Date (Date)
  - Target Date (Date)

Views:
  - Roadmap (Roadmap View)
  - Timeline (Table View)
```

#### OKR Tracker Template

```yaml
Fields:
  - Status: Not Started, On Track, At Risk, Completed
  - Objective (Single select): O1, O2, O3
  - Key Result (Text): Key result description
  - Progress (Number): Progress percentage
  - Owner (People): Assignee
  - Quarter (Single select): Q1, Q2, Q3, Q4

Views:
  - OKR Dashboard (Table View, grouped by Objective)
  - Progress Overview (Table View, grouped by Status)
```

#### Release Manager Template

```yaml
Fields:
  - Status: Planning, Development, Testing, Ready, Released
  - Version (Single select): v1.0, v1.1, v2.0
  - Release Date (Date)
  - Release Type (Single select): Major, Minor, Patch
  - Breaking Changes (Single select): Yes, No

Views:
  - Release Board (Board View)
  - Release Roadmap (Roadmap View)
  - Version History (Table View)
```

### Template Selection Guide

| Project Type | Recommended Template | Applicable Scenario |
|--------------|---------------------|---------------------|
| Feature Development | Feature Tracker | Track new feature development progress |
| Defect Management | Bug Tracker | Manage and track software defects |
| Long-term Planning | Roadmap | Plan product roadmap and version releases |
| Goal Management | OKR Tracker | Track team goals and key results |
| Version Release | Release Manager | Manage version release process |
| Agile Development | Custom Agile Template | Manage Sprint and user stories |

### Custom Templates

You can create your own project templates:

**Step 1: Create Base Project**

1. Create new project and configure all needed fields
2. Create multiple views
3. Configure automation rules

**Step 2: Save as Template**

1. Enter project settings
2. Click **Save as template**
3. Enter template name and description

**Step 3: Use Template**

Select custom template when creating new project.

### Team Template Design

**Agile Team Template:**

```yaml
Fields:
  - Status: Backlog, Sprint Backlog, In Progress, Review, Testing, Done
  - Sprint (Iteration)
  - Story Points (Number)
  - Priority: Critical, High, Medium, Low
  - Type: User Story, Bug, Task, Spike
  - Epic (Single select)

Views:
  - Sprint Board (Board View, grouped by Status)
  - Sprint Planning (Table View, grouped by Sprint)
  - Roadmap (Roadmap View, grouped by Epic)
  - My Tasks (Table View, filter assignee:@me)
```

**Open Source Project Template:**

```yaml
Fields:
  - Status: Triage, Accepted, In Progress, Review, Done
  - Priority: Critical, High, Medium, Low
  - Type: Bug, Feature, Enhancement, Documentation
  - Good First Issue (Single select: Yes, No)
  - Help Wanted (Single select: Yes, No)

Views:
  - Main Board (Board View)
  - Contributor Tasks (Table View, filter Good First Issue = Yes)
  - Bug Tracker (Table View, filter Type = Bug)
```

---

## 10. GitHub Projects vs Jira Comparison

### Feature Comparison

| Feature | GitHub Projects | Jira |
|---------|----------------|------|
| Price | Free (public projects) / Pro (private projects) | Free (under 10 people) / Paid |
| Learning Curve | Low | Medium to High |
| Integration | GitHub Native Integration | Rich third-party integrations |
| Customization | Medium | Highly customizable |
| Workflow | Simple and intuitive | Complex and powerful |
| Reports | Basic charts | Rich reports |
| API | GraphQL | REST + GraphQL |
| Automation | Built-in + Actions | Built-in + Plugins |
| Suitable Team Size | Small to Medium | Medium to Large |
| Agile Support | Basic | Complete |

### Advantages and Disadvantages

**GitHub Projects Advantages:**

- **Seamless Integration**: Deep integration with GitHub's Issues, PR, Actions, no need to switch tools
- **Zero Cost Entry**: Public projects completely free, private projects also free in Pro plan
- **Simple and Easy to Use**: Intuitive interface, low learning cost, new members can quickly get started
- **Real-time Collaboration**: Multiple people can edit simultaneously, changes sync in real-time
- **Developer Friendly**: High automation through GraphQL API and GitHub Actions

**GitHub Projects Disadvantages:**

- **Relatively Simple Features**: Lacks complex custom workflows and advanced reports
- **Limited Report Capabilities**: Fewer built-in chart types, complex analysis needs API
- **No Subtask Support**: Cannot create task hierarchy
- **Limited Custom Fields**: Fewer field types, cannot meet complex needs

**Jira Advantages:**

- **Comprehensive Features**: Supports complex custom workflows, fields and interfaces
- **Powerful Reports**: Built-in rich reports and dashboards
- **Subtask Support**: Supports multi-level task structure
- **Plugin Ecosystem**: Rich third-party plugins to extend functionality

**Jira Disadvantages:**

- **High Learning Cost**: Complex features, tedious configuration
- **Higher Price**: Large teams need to pay
- **Weak Code Integration**: Integration with code hosting platforms needs additional configuration
- **Performance Issues**: Large projects may experience performance degradation

### Selection Suggestions

**Choose GitHub Projects If:**

- Team is already using GitHub
- Project scale is small or medium
- Want simple and easy to use tool
- Limited budget
- Open source project

**Choose Jira If:**

- Need complex custom workflows
- Large teams and complex projects
- Need detailed reports and analysis
- Need to integrate with multiple tools
- Enterprise-level project management needs

### Migration Suggestions

If migrating from Jira to GitHub Projects:

1. **Evaluate Needs**: List core features used in Jira
2. **Field Mapping**: Map Jira fields to GitHub Projects fields
3. **Simplify Workflow**: Simplify complex workflows
4. **Data Migration**: Use API to batch import data
5. **Train Team**: Provide GitHub Projects training

---

## 11. Team Project Management Best Practices

### Project Structure Design

**Recommended Project Structure:**

```
Organization-level Projects (Cross-team)
├── Product Roadmap
├── Quarterly Goals
└── Cross-team Coordination

Team-level Projects (Single team)
├── Sprint Board
├── Bug Tracking
└── Technical Debt

Personal-level Projects (Individual)
├── Personal Tasks
└── Learning Plan
```

### Workflow Design

**Standard Agile Workflow:**

```
Backlog → Sprint Backlog → In Progress → Code Review → Testing → Done
```

**Simplified Workflow:**

```
To Do → In Progress → Done
```

**Detailed Workflow (Suitable for Large Projects):**

```
Triage → Ready → In Development → Code Review → QA Testing → 
UAT → Ready to Deploy → Deployed → Done
```

**Workflow Design Principles:**

When designing workflow, should follow the following principles to ensure process is clear and efficient:

1. **Limited States**: Each workflow should not have too many states, recommend 4-7 states
2. **One-way Flow**: Tasks usually flow from left to right, avoid frequent rollbacks
3. **Clear Entry**: Each state should have clear entry conditions
4. **Clear Exit**: Each state should have clear completion criteria
5. **Avoid Bottlenecks**: Identify states that may cause task backlog, set WIP limits

**Workflow Selection for Different Teams:**

| Team Type | Recommended Workflow | State Count |
|-----------|---------------------|-------------|
| Startup Team | Simplified Workflow | 3-4 states |
| Mature Product Team | Standard Agile Workflow | 5-6 states |
| Enterprise Team | Detailed Workflow | 7-9 states |
| Open Source Project | Simplified Workflow + Classification Labels | 4-5 states |

### Naming Conventions

**Project Naming:**
```
[Team]-[Project Type]-[Description]
Examples:
- frontend-sprint-board
- backend-bug-tracker
- product-roadmap-2024
```

**Field Naming:**
```
Use clear, consistent naming
Examples:
- Status (not state or phase)
- Priority (not priority-level)
- Story Points (not points or sp)
```

**View Naming:**
```
[Purpose]-[Filter Condition]
Examples:
- My Tasks
- Sprint Board
- High Priority
```

### Permission Management

**Permission Levels:**

| Role | Permission | Applicable Personnel |
|------|-----------|---------------------|
| Admin | Full Control | Project Manager |
| Write | Edit Project Items | Developers |
| Read | Read-only Access | Stakeholders |

**Permission Setting Suggestions:**

1. **Project Manager**: Admin permission
2. **Developers**: Write permission
3. **Testers**: Write permission
4. **Product Manager**: Write or Admin permission
5. **External Personnel**: Read permission

### Communication and Collaboration

**Daily Stand-up:**

1. Use board view to display current Sprint
2. Team members update task status
3. Identify blockers and risks

**Sprint Planning:**

1. Use table view to evaluate workload
2. Assign tasks to Sprint
3. Set priorities

**Sprint Review:**

1. Analyze completion status
2. Identify improvement points
3. Adjust next Sprint plan

---

## 12. Project Data Analysis and Reports

### Built-in Charts

GitHub Projects provides multiple built-in charts to help analyze project data.

#### Burndown Chart

Burndown chart shows the trend of remaining workload during Sprint.

**Configuration:**

```yaml
Chart Type: Burndown
Time Range: Current iteration
Workload Field: Story Points
```

**Interpretation:**

- **Ideal Line**: Trend line assuming uniform task completion
- **Actual Line**: Actual remaining workload
- **Above Ideal Line**: Progress behind
- **Below Ideal Line**: Progress ahead

#### Cumulative Flow Diagram

Cumulative flow diagram shows the change in task count per status over time.

**Configuration:**

```yaml
Chart Type: Cumulative Flow
Time Range: Last 30 days
Group Field: Status
```

**Interpretation:**

- **Bandwidth Widening**: Tasks in that status are increasing, may have bottleneck
- **Bandwidth Stable**: Workflow is stable
- **Bandwidth Narrowing**: Tasks in that status are decreasing

#### Pie Chart

Pie chart shows task distribution.

**Configuration:**

```yaml
Chart Type: Pie
Group Field: Priority
Filter: -status:done
```

**Common Analysis:**

- Distribution by priority: Understand current incomplete tasks' priority distribution, identify if need to adjust resources
- Distribution by assignee: View each member's task assignment situation, balance workload
- Distribution by type: Analyze proportion of Bug, Feature, Enhancement etc. types
- Distribution by label: Identify task's technical domain distribution, like frontend, backend, database etc.

#### Bar Chart

Bar chart shows statistical information of numerical fields.

**Configuration:**

```yaml
Chart Type: Bar
X Axis: Assignees
Y Axis: Story Points (Sum)
Filter: sprint:"current iteration"
```

**Common Usage of Bar Chart:**

- **Workload Distribution**: Sum Story Points by assignee, identify uneven workload
- **Completion Comparison**: Compare planned vs actual completed Story Points
- **Trend Analysis**: Display task completion trends by time dimension

### Chart Combination Analysis

Through combining multiple charts, can build complete project dashboard:

**Dashboard Configuration Suggestions:**

| Chart | Type | Purpose |
|-------|------|---------|
| Task Status Distribution | Pie | View each status task proportion |
| Priority Distribution | Pie | Identify high priority task count |
| Team Workload | Bar | Compare each member's workload |
| Sprint Progress | Burndown | Track Sprint completion trend |
| Status Change Trend | Cumulative Flow | Identify workflow bottlenecks |

### Custom Reports

Use GitHub API to create custom reports:

```graphql
# GraphQL Query Example
query {
  user(login: "my-org") {
    projectV2(number: 1) {
      items(first: 100) {
        nodes {
          content {
            ... on Issue {
              title
              state
              labels(first: 10) {
                nodes {
                  name
                }
              }
            }
          }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field {
                  ... on ProjectV2SingleSelectField {
                    name
                  }
                }
              }
              ... on ProjectV2ItemFieldNumberValue {
                number
                field {
                  ... on ProjectV2Field {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Key Metrics

**Agile Metrics:**

| Metric | Calculation Method | Target |
|--------|-------------------|--------|
| Velocity | Average completed story points over past 3-5 Sprints | Stable |
| Completion Rate | Completed story points / Planned story points | > 80% |
| Cycle Time | Average time from start to completion | As short as possible |
| Cumulative Flow | Task count per status | Keep stable |

**Quality Metrics:**

| Metric | Calculation Method | Target |
|--------|-------------------|--------|
| Defect Density | Bug count / Feature count | As low as possible |
| Fix Time | Average time from discovery to fix | As short as possible |
| Regression Rate | Reopened Bugs / Total Bugs | < 5% |

---

## 13. Cross-repo Project Management

### Create Cross-repo Project

GitHub Projects can manage work items from multiple repositories. This is very useful in microservice architecture, multi-repo projects or organization-level project management.

**Typical Scenarios for Cross-repo Projects:**

- **Microservice Architecture**: Frontend, backend, database etc. in different repositories
- **Multi-platform Applications**: iOS, Android, Web etc. platforms developed separately
- **Infrastructure Projects**: API, SDK, documentation, examples etc. maintained separately
- **Organization-level Management**: Unified view across teams and projects

**Step 1: Create Project**

Create project at organization level (not repository level):

```bash
# Create organization project using CLI
gh project create --title "Cross-Repo Project" --owner my-org
```

**Step 2: Add Issues from Multiple Repositories**

1. Open project
2. Click **+ Add item**
3. Select **Add items from repository**
4. Select different repositories
5. Select Issues to add

**Step 3: Use Repository Field**

Project will automatically add Repository field, showing which repository each entry belongs to.

### Cross-repo Views

**Group by Repository:**

```
View Name: By Repository
Group: Repository
Display Fields: Title, Status, Priority, Assignee
```

**Group by Team (Using Labels):**

```
View Name: By Team
Group: Team (Custom single select field)
Filter: -status:done
```

### Cross-repo Automation

Use GitHub Actions to achieve cross-repo automation:

```yaml
# .github/workflows/sync-project.yml
name: Sync Cross-Repo Project

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday 9am
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Sync issues from multiple repos
        uses: actions/github-script@v7
        with:
          script: |
            const repos = ['repo-frontend', 'repo-backend', 'repo-mobile'];
            const projectId = 'PVT_xxxxx';
            
            for (const repo of repos) {
              const issues = await github.rest.issues.listForRepo({
                owner: context.repo.owner,
                repo: repo,
                state: 'open',
                labels: 'sprint-ready'
              });
              
              for (const issue of issues.data) {
                // Add to project
                await github.graphql(`
                  mutation($projectId: ID!, $contentId: ID!) {
                    addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
                      item {
                        id
                      }
                    }
                  }
                `, {
                  projectId: projectId,
                  contentId: issue.node_id
                });
              }
            }
```

### Cross-repo Project Best Practices

1. **Unified Labels**: Use unified label system across repos, ensure classification consistency
2. **Standardized Issue Templates**: Use similar Issue templates in each repo, for summary analysis
3. **Clear Naming**: Project and view naming clear and easy to understand, reflecting cross-repo characteristics
4. **Regular Sync**: Ensure all repos' Issues are synced to project
5. **Permission Management**: Reasonably set cross-repo access permissions, ensure team members can access needed repos
6. **Use Repository Field**: Use auto-added Repository field for filtering and grouping
7. **Create Repo-specific Views**: Create independent views for each repo, convenient for each team to view
8. **Unified Workflow**: Try to use unified status fields and workflow, reduce management complexity

**Cross-repo Project Challenges and Solutions:**

| Challenge | Solution |
|-----------|----------|
| Labels not unified | Create organization-level label template, unify naming conventions |
| Complex permission management | Use team permission management, batch set access permissions |
| Too many notifications | Filter notifications by repo or label, reduce interference |
| Large data volume | Use filter and grouping functions, only show related data |

---

## 14. GitHub Projects + Actions Integration

### Automation Scenarios

GitHub Projects integration with GitHub Actions can achieve complex automation workflows. Here are some common automation scenarios:

#### Auto-add Issue to Project

When new Issue is created, automatically add to specified project. This is particularly useful for projects with large numbers of Issues, ensuring all Issues are included in project management scope.

```yaml
# .github/workflows/auto-add-to-project.yml
name: Auto Add to Project

on:
  issues:
    types: [opened]

jobs:
  add-to-project:
    runs-on: ubuntu-latest
    steps:
      - name: Add issue to project
        uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/users/my-org/projects/1
          github-token: ${{ secrets.GITHUB_TOKEN }}
          labeled: sprint-ready
```

#### Auto-update Project Status

```yaml
# .github/workflows/update-project-status.yml
name: Update Project Status

on:
  issues:
    types: [closed]
  pull_request:
    types: [closed]

jobs:
  update-status:
    runs-on: ubuntu-latest
    steps:
      - name: Get project item ID
        id: get-item
        uses: actions/github-script@v7
        with:
          script: |
            // Get project item ID
            const issue = context.payload.issue || context.payload.pull_request;
            const projectId = 'PVT_xxxxx';
            
            const result = await github.graphql(`
              query($projectId: ID!) {
                node(id: $projectId) {
                  ... on ProjectV2 {
                    items(first: 100) {
                      nodes {
                        id
                        content {
                          ... on Issue {
                            id
                          }
                          ... on PullRequest {
                            id
                          }
                        }
                      }
                    }
                  }
                }
              }
            `, { projectId });
            
            const itemId = result.node.items.nodes.find(
              item => item.content.id === issue.node_id
            )?.id;
            
            return itemId;

      - name: Update status to Done
        if: steps.get-item.outputs.result
        uses: actions/github-script@v7
        with:
          script: |
            const projectId = 'PVT_xxxxx';
            const itemId = '${{ steps.get-item.outputs.result }}';
            const statusFieldId = 'PVTF_xxxxx';
            
            await github.graphql(`
              mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: ProjectV2FieldValue!) {
                updateProjectV2ItemFieldValue(input: {
                  projectId: $projectId
                  itemId: $itemId
                  fieldId: $fieldId
                  value: $value
                }) {
                  projectV2Item {
                    id
                  }
                }
              }
            `, {
              projectId,
              itemId,
              fieldId: statusFieldId,
              value: { singleSelectOptionId: 'done_option_id' }
            });
```

#### Auto-assign Iteration

```yaml
# .github/workflows/auto-assign-sprint.yml
name: Auto Assign Sprint

on:
  issues:
    types: [opened]

jobs:
  assign-sprint:
    runs-on: ubuntu-latest
    steps:
      - name: Assign to current sprint
        uses: actions/github-script@v7
        with:
          script: |
            // Get current iteration
            const projectId = 'PVT_xxxxx';
            const sprintFieldId = 'PVTF_xxxxx';
            
            // Get current iteration option ID
            const result = await github.graphql(`
              query($projectId: ID!) {
                node(id: $projectId) {
                  ... on ProjectV2 {
                    fields(first: 20) {
                      nodes {
                        ... on ProjectV2IterationField {
                          id
                          configuration {
                            iterations {
                              id
                              startDate
                              duration
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            `, { projectId });
            
            // Calculate current iteration
            const iterations = result.node.fields.nodes.find(
              f => f.id === sprintFieldId
            ).configuration.iterations;
            
            const today = new Date();
            const currentIteration = iterations.find(iter => {
              const start = new Date(iter.startDate);
              const end = new Date(start);
              end.setDate(end.getDate() + iter.duration);
              return today >= start && today < end;
            });
            
            return currentIteration?.id;
```

### Advanced Integration Scenarios

#### Auto-close Issue and Update Project when PR Merged

```yaml
# .github/workflows/pr-merged.yml
name: PR Merged

on:
  pull_request:
    types: [closed]

jobs:
  update-project:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Get linked issues
        id: get-issues
        uses: actions/github-script@v7
        with:
          script: |
            const pr = context.payload.pull_request;
            const body = pr.body || '';
            
            // Extract associated Issue numbers from PR description
            const issueNumbers = [];
            const patterns = [
              /(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)/gi,
              /(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+(?:https:\/\/github\.com\/[^\/]+\/[^\/]+\/issues\/(\d+))/gi
            ];
            
            for (const pattern of patterns) {
              let match;
              while ((match = pattern.exec(body)) !== null) {
                issueNumbers.push(match[1]);
              }
            }
            
            return issueNumbers;

      - name: Update project items
        if: steps.get-issues.outputs.result != '[]'
        uses: actions/github-script@v7
        with:
          script: |
            const issueNumbers = JSON.parse('${{ steps.get-issues.outputs.result }}');
            const projectId = 'PVT_xxxxx';
            
            for (const issueNumber of issueNumbers) {
              // Get Issue's project item
              // Update status to Done
              // Set completion date
            }
```

#### Scheduled Report Generation

```yaml
# .github/workflows/weekly-report.yml
name: Weekly Project Report

on:
  schedule:
    - cron: '0 17 * * 5'  # Every Friday 5pm
  workflow_dispatch:

jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - name: Generate report
        uses: actions/github-script@v7
        with:
          script: |
            const projectId = 'PVT_xxxxx';
            
            // Query project data
            const result = await github.graphql(`
              query($projectId: ID!) {
                node(id: $projectId) {
                  ... on ProjectV2 {
                    items(first: 200) {
                      nodes {
                        content {
                          ... on Issue {
                            title
                            state
                          }
                        }
                        fieldValues(first: 20) {
                          nodes {
                            ... on ProjectV2ItemFieldSingleSelectValue {
                              name
                              field { ... on ProjectV2SingleSelectField { name } }
                            }
                            ... on ProjectV2ItemFieldIterationValue {
                              title
                              startDate
                              duration
                              field { ... on ProjectV2IterationField { name } }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            `, { projectId });
            
            // Generate report
            const items = result.node.items.nodes;
            const completed = items.filter(i => 
              i.fieldValues.nodes.some(f => 
                f.field?.name === 'Status' && f.name === 'Done'
              )
            );
            
            const report = `
            # Weekly Report - ${new Date().toISOString().split('T')[0]}
            
            ## This Week's Completion
            - Completed tasks: ${completed.length}
            - Completion rate: ${((completed.length / items.length) * 100).toFixed(1)}%
            
            ## Pending Tasks
            - Pending tasks: ${items.length - completed.length}
            `;
            
            // Create Issue as report
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `Weekly Report - ${new Date().toISOString().split('T')[0]}`,
              body: report,
              labels: ['weekly-report']
            });
```

---

## 15. Practice: Manage an Open Source Project

### Scenario Setup

Suppose you are managing an open source project called `awesome-app`, need to use GitHub Projects for project management. The project has the following characteristics:

- **Project Type**: Full-stack Web application
- **Team Size**: 5 core maintainers + community contributors
- **Repository Structure**: Frontend (React), Backend (Node.js), Documentation (Docs)
- **Release Cycle**: Every two weeks one version
- **Contributor Count**: About 50 active contributors

### Step 1: Create Project

**1. Create Organization-level Project**

```bash
# Create using CLI
gh project create --title "Awesome App Development" --owner my-org
```

**2. Configure Fields**

Add the following custom fields:

| Field Name | Type | Options |
|------------|------|---------|
| Priority | Single select | Critical, High, Medium, Low |
| Type | Single select | Bug, Feature, Enhancement, Documentation |
| Sprint | Iteration | 2-week cycle |
| Story Points | Number | 1, 2, 3, 5, 8, 13 |
| Good First Issue | Single select | Yes, No |
| Help Wanted | Single select | Yes, No |
| Release | Single select | v1.0, v1.1, v2.0 |

**3. Create Views**

```
View 1: Main Board (Board View)
- Group: Status
- Filter: None
- Sort: Priority (Descending)

View 2: Sprint Planning (Table View)
- Group: Sprint
- Filter: -status:done
- Sort: Priority (Descending)

View 3: Bug Tracker (Table View)
- Group: Priority
- Filter: Type = Bug -status:done
- Sort: Priority (Descending)

View 4: Good First Issues (Table View)
- Group: Type
- Filter: Good First Issue = Yes -status:done

View 5: Roadmap (Roadmap View)
- Time Range: Release
```

### Step 2: Configure Automation

**1. Built-in Automation Rules**

```
Rule 1: Issue added to project → Status = Triage
Rule 2: Issue labeled "accepted" → Status = Accepted
Rule 3: PR created and linked Issue → Status = In Progress
Rule 4: PR merged → Status = Done
Rule 5: Issue closed → Status = Done
```

**2. GitHub Actions Automation**

```yaml
# .github/workflows/project-setup.yml
name: Project Setup

on:
  issues:
    types: [opened, labeled]

jobs:
  auto-triage:
    if: github.event.action == 'opened'
    runs-on: ubuntu-latest
    steps:
      - name: Add to project
        uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/orgs/my-org/projects/1
          github-token: ${{ secrets.GITHUB_TOKEN }}

  auto-accept:
    if: github.event.label.name == 'accepted'
    runs-on: ubuntu-latest
    steps:
      - name: Update status to Accepted
        uses: actions/github-script@v7
        with:
          script: |
            // Update project item status
```

### Step 3: Issue and PR Templates

**Issue Templates:**

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
description: Report a bug
labels: ["type:bug", "triage"]
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Describe the bug
    validations:
      required: true
  
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the behavior
    validations:
      required: true
  
  - type: dropdown
    id: severity
    attributes:
      label: Severity
      options:
        - Critical
        - High
        - Medium
        - Low
    validations:
      required: true
```

```yaml
# .github/ISSUE_TEMPLATE/feature_request.yml
name: Feature Request
description: Request a new feature
labels: ["type:feature"]
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Describe the feature
    validations:
      required: true
  
  - type: textarea
    id: motivation
    attributes:
      label: Motivation
      description: Why is this feature important?
    validations:
      required: true
```

### Step 4: Sprint Management Process

**Sprint Planning (Monday):**

1. Use Sprint Planning view
2. Select tasks from Backlog
3. Assign to current Sprint
4. Set Story Points
5. Assign assignee

**Daily Stand-up:**

1. Use Main Board view
2. Team members update task status
3. Identify blockers and risks

**Sprint Review (Friday):**

1. Analyze completion status
2. Calculate velocity and completion rate
3. Identify improvement points
4. Plan next Sprint

### Step 5: Community Contribution Management

**Optimize for New Contributors:**

1. Use Good First Issues view
2. Label simple tasks with "good first issue"
3. Provide detailed Issue descriptions
4. Set "help wanted" label to request help

**Contribution Process:**

```
1. Contributor Forks repository
2. Select Good First Issues
3. Create Pull Request
4. Code review
5. Merge and update project status
```

**Community Contribution Management Best Practices:**

Managing open source project community contributions requires special attention and strategy. Here are some proven best practices:

1. **Create Welcome View**: Create a view specifically for new contributors, only showing tasks marked as "good first issue", and provide detailed getting started guide
2. **Respond Promptly**: Give initial reply to new contributors' Issues and PRs within 48 hours
3. **Detailed Guidance**: Provide clear task description, acceptance criteria and related code locations in Issue description
4. **Label System**: Use labels to help contributors find suitable tasks
   - `good first issue`: Simple tasks suitable for new contributors
   - `help wanted`: Tasks needing community help
   - `documentation`: Documentation related tasks
   - `bug`: Defect fix tasks
5. **Contributing Guide**: Maintain CONTRIBUTING.md file in repository, explaining contribution process and code standards
6. **Recognize Contributors**: Thank contributors in release notes, build positive community atmosphere

**Contributor Label System Design:**

| Label | Color | Description |
|-------|-------|-------------|
| good first issue | Purple | Simple tasks for new contributors |
| help wanted | Green | Tasks needing community help |
| documentation | Blue | Documentation related tasks |
| bug | Red | Defect fix tasks |
| enhancement | Yellow | Feature enhancement tasks |
| question | Grey | Question consultation |
| wontfix | Black | Issues that won't be fixed |

### Step 6: Version Release Management

**Using Release Field:**

1. Assign target version to each Issue
2. Use Roadmap view to view version plan
3. Use filter function to view tasks for specific version

**Release Checklist:**

```
Filter: Release = v1.0 -status:done
```

Check if all v1.0 tasks are completed.

### Step 7: Project Reports

**Weekly Report Generation:**

```bash
# Use CLI to get project data
gh project item-list 1 --owner my-org --format json | \
  jq '[.items[] | select(.status == "Done")] | length'
```

**Monthly Analysis:**

- Completed task count
- Bug fix rate
- New contributor count
- Community activity

---

## Summary

GitHub Projects is a powerful and easy-to-use project management tool, especially suitable for GitHub users. Through this article's learning, you should be able to:

1. **Understand GitHub Projects Core Concepts**: Views, fields, automation
2. **Create and Configure Projects**: Choose appropriate templates and configurations
3. **Use Different Views**: Table, Board, Roadmap
4. **Custom Fields**: Create various field types based on needs
5. **Configure Automation**: Reduce manual operations, improve efficiency
6. **Integrate Issues and PRs**: Achieving seamless connection between code development and project management
7. **Manage Iterations**: Support agile development processes
8. **Analyze Project Data**: Use charts and reports to track progress
9. **Cross-repo Management**: Manage projects across multiple repositories
10. **Integrate with Actions**: Achieving advanced automation

### Further Learning

- [GitHub Projects Official Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Projects API Documentation](https://docs.github.com/en/graphql/reference/objects#projectv2)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Agile Development Practice Guide](https://www.atlassian.com/agile)
