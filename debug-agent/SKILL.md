---
name: debug-workflow
description: Debugging workflow with Playwright browser automation for end-to-end testing, visual verification, and interactive debugging of web applications and MCP tools.
version: "2.0"
date: 2026-03-12
license: MIT
---

# Debug Workflow

Workflow for browser-based debugging, end-to-end testing, and visual verification using Playwright.

## When to Use This Skill

Use this skill when:
- Testing MCP tools that interact with web UIs (Moodle, WordPress, n8n)
- Debugging visual issues in web applications
- Verifying that API calls produce correct UI results
- Creating automated test scenarios
- Capturing evidence of bugs or successful fixes

## Core Capabilities

### 1. Playwright Browser Automation

Use the MCP browser tools (Playwright-based) for all browser interactions:

```javascript
// Available tools via MCP (prefixed with mcp__MCP_DOCKER__)
mcp__MCP_DOCKER__browser_navigate     // Go to URL
mcp__MCP_DOCKER__browser_snapshot     // Get accessibility tree (preferred)
mcp__MCP_DOCKER__browser_click        // Click elements
mcp__MCP_DOCKER__browser_type         // Type text
mcp__MCP_DOCKER__browser_fill_form    // Fill multiple fields
mcp__MCP_DOCKER__browser_take_screenshot  // Visual capture
mcp__MCP_DOCKER__browser_wait_for     // Wait for text/conditions
mcp__MCP_DOCKER__browser_console_messages // Check for JS errors
mcp__MCP_DOCKER__browser_network_requests // Monitor API calls
```

## Workflow: Debug MCP Tool via UI

### Phase 1: Setup Test Environment

```markdown
## Debug Session Setup

**Tool Under Test:** moodle_create_quiz
**Target URL:** https://moodle.dirk-schulenburg.net
**Test Course:** LF4 Weinhandlung (ID: 8)
**Expected Outcome:** Quiz visible in section 1
```

### Phase 2: Manual Verification via Browser

```javascript
// 1. Navigate to Moodle course
mcp__MCP_DOCKER__browser_navigate({ url: "https://moodle.dirk-schulenburg.net/course/view.php?id=8" })

// 2. Get page structure
mcp__MCP_DOCKER__browser_snapshot()

// 3. Take screenshot as evidence
mcp__MCP_DOCKER__browser_take_screenshot({ filename: "quiz-created.png" })
```

### Phase 3: Check for Errors

```javascript
// Check browser console for JS errors
mcp__MCP_DOCKER__browser_console_messages({ onlyErrors: true })

// Check network requests for failed API calls
mcp__MCP_DOCKER__browser_network_requests({ urlPattern: "webservice" })
```

## Debugging Scenarios

### Scenario 1: MCP Tool Returns Success but UI Shows Nothing

```markdown
## Debug Steps

1. **Verify API Response**
   - Check MCP tool response for IDs
   - Note: quizId, cmid values

2. **Check Direct URL**
   mcp__MCP_DOCKER__browser_navigate({ url: "https://moodle.dirk-schulenburg.net/mod/quiz/view.php?id={cmid}" })
   - If works: Quiz exists but not visible in course
   - If 404: Quiz creation failed silently

3. **Check Course Edit Mode**
   - Some items only visible in edit mode
   mcp__MCP_DOCKER__browser_click({ ref: "edit-mode-toggle" })
   mcp__MCP_DOCKER__browser_snapshot()

4. **Check User Permissions**
   - API user might see different than admin
   - Login as test user and verify
```

### Scenario 2: Visual Layout Bug

```markdown
## Debug Steps

1. **Take Full Page Screenshot**
   mcp__MCP_DOCKER__browser_take_screenshot({ fullPage: true, filename: "layout-bug.png" })

2. **Inspect Element**
   mcp__MCP_DOCKER__browser_snapshot({ ref_id: "problematic-element" })

3. **Check Responsive Behavior**
   mcp__MCP_DOCKER__browser_resize({ width: 768, height: 1024 })
   mcp__MCP_DOCKER__browser_take_screenshot({ filename: "tablet-view.png" })

4. **Check CSS Console Errors**
   mcp__MCP_DOCKER__browser_console_messages({ pattern: "CSS" })
```

### Scenario 3: Form Submission Failure

```markdown
## Debug Steps

1. **Fill Form Step by Step**
   mcp__MCP_DOCKER__browser_fill_form({
     fields: [
       { name: "Quiz Name", type: "textbox", ref: "input-name", value: "Test Quiz" },
       { name: "Time Limit", type: "textbox", ref: "input-time", value: "60" }
     ]
   })

2. **Monitor Network on Submit**
   mcp__MCP_DOCKER__browser_network_requests()  // Clear first

3. **Click Submit**
   mcp__MCP_DOCKER__browser_click({ ref: "submit-button" })
   mcp__MCP_DOCKER__browser_wait_for({ time: 3 })

4. **Check Network Response**
   mcp__MCP_DOCKER__browser_network_requests({ urlPattern: "quiz" })

5. **Check for Error Messages**
   mcp__MCP_DOCKER__browser_snapshot()
```

## Testing MCP Servers

### WordPress MCP Testing

```javascript
// Test wp_create_post via UI verification
// 1. Call MCP tool (via Claude)
// Result: { postId: 123, url: "https://..." }

// 2. Verify in browser
mcp__MCP_DOCKER__browser_navigate({ url: "https://cannabis-kultur.online/wp-admin/post.php?post=123&action=edit" })
mcp__MCP_DOCKER__browser_snapshot()

// 3. Check frontend
mcp__MCP_DOCKER__browser_navigate({ url: "https://cannabis-kultur.online/?p=123" })
mcp__MCP_DOCKER__browser_take_screenshot({ filename: "new-post-frontend.png" })
```

### Moodle MCP Testing

```javascript
// Test moodle_create_section via UI verification
// 1. Call MCP tool
// Result: { sectionId: 5 }

// 2. Navigate to course
mcp__MCP_DOCKER__browser_navigate({ url: "https://moodle.dirk-schulenburg.net/course/view.php?id=8" })

// 3. Verify section exists
mcp__MCP_DOCKER__browser_snapshot()

// 4. Check section content
mcp__MCP_DOCKER__browser_click({ ref: "section-5-toggle" })
mcp__MCP_DOCKER__browser_take_screenshot({ filename: "section-5-content.png" })
```

### n8n Workflow Testing

```javascript
// Test workflow execution via UI
// 1. Navigate to n8n
mcp__MCP_DOCKER__browser_navigate({ url: "https://n8n.dirk-schulenburg.net" })

// 2. Find workflow
mcp__MCP_DOCKER__browser_snapshot()
mcp__MCP_DOCKER__browser_click({ ref: "workflow-email-router" })

// 3. Check execution history
mcp__MCP_DOCKER__browser_click({ ref: "executions-tab" })
mcp__MCP_DOCKER__browser_snapshot()

// 4. Check for errors
mcp__MCP_DOCKER__browser_take_screenshot({ filename: "n8n-execution-log.png" })
```

## Error Documentation

### Screenshot Naming Convention

```
{date}_{tool}_{status}.png

Examples:
2026-01-19_moodle_create_quiz_success.png
2026-01-19_moodle_create_quiz_error_404.png
2026-01-19_wp_create_post_validation_error.png
```

### Bug Report Template

```markdown
## Bug Report

**Date:** 2026-01-19
**Tool:** moodle_create_quiz
**Severity:** High

### Steps to Reproduce
1. Call moodle_create_quiz with courseId=8, sectionNum=1, quizName="Test"
2. Tool returns success with quizId=15
3. Navigate to course view

### Expected Result
Quiz "Test" visible in section 1

### Actual Result
Quiz not visible. Direct URL returns 404.

### Evidence
- Screenshot: debug-session/moodle_create_quiz_error_404.png
- Console: No JS errors
- Network: POST to webservice returned 200 but response contains "exception"

### API Response
{
  "exception": "webservice_access_exception",
  "message": "Access denied"
}

### Root Cause
Missing capability: moodle/quiz:addinstance for webservice user
```

## Quick Reference

### Common Selectors for Target Sites

#### Moodle
```javascript
// Login
ref: "username-input", "password-input", "login-button"

// Course view
ref: "edit-mode-toggle", "section-{n}", "add-activity"

// Quiz
ref: "quiz-name-input", "quiz-submit", "quiz-question-{n}"
```

#### WordPress Admin
```javascript
// Login
ref: "user-login", "user-pass", "wp-submit"

// Post editor
ref: "post-title-input", "content-editor", "publish-button"

// Media library
ref: "upload-button", "media-library-grid"
```

#### n8n
```javascript
// Workflow list
ref: "workflow-{name}", "new-workflow-button"

// Execution
ref: "execute-workflow", "executions-tab", "execution-{id}"
```

### Debug Checklist

```markdown
- [ ] Browser console checked for errors
- [ ] Network requests inspected
- [ ] Element exists in DOM (snapshot)
- [ ] Element visible (screenshot)
- [ ] Form validation passed
- [ ] API response correct
- [ ] UI reflects API state
- [ ] Permissions verified
- [ ] Screenshots saved
- [ ] Bug report created (if issue found)
```

---

*Debug Workflow v2.0*
