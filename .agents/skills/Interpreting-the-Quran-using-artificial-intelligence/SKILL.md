```markdown
# Interpreting-the-Quran-using-artificial-intelligence Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill provides guidance on contributing to the `Interpreting-the-Quran-using-artificial-intelligence` TypeScript codebase. It covers coding conventions, commit patterns, workflows for dependency management, and testing practices. The repository focuses on leveraging artificial intelligence to interpret the Quran, with an emphasis on maintainable TypeScript code and regular dependency updates.

## Coding Conventions

### File Naming
- Use **camelCase** for file names.
  - Example: `quranInterpreter.ts`, `aiHelperFunctions.ts`

### Import Style
- Use **relative imports** for modules within the project.
  - Example:
    ```typescript
    import { analyzeVerse } from './verseAnalyzer';
    ```

### Export Style
- Use **named exports** for functions, constants, and types.
  - Example:
    ```typescript
    // In verseAnalyzer.ts
    export function analyzeVerse(verse: string): AnalysisResult { ... }
    ```

### Commit Patterns
- Commit messages are mixed in style but often use the `fix` prefix for bug fixes.
- Average commit message length: ~51 characters.
  - Example: `fix: correct verse parsing logic for edge cases`

## Workflows

### Update Frontend Dependencies
**Trigger:** When you need to upgrade, fix, or synchronize frontend npm dependencies (e.g., to address security vulnerabilities or keep dependencies up-to-date).  
**Command:** `/update-frontend-deps`

1. Modify `frontend/package.json` to update dependency versions as needed.
2. Regenerate `frontend/package-lock.json` to ensure it reflects the updated dependencies.
   - Run:  
     ```sh
     cd frontend
     npm install
     ```
3. Optionally update `frontend/tsconfig.json` if any dependency changes require adjustments to TypeScript configuration.
4. Commit the changes with a descriptive message, e.g., `fix: update frontend dependencies to latest versions`.

**Files Involved:**
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/tsconfig.json` (optional)

**Frequency:** About twice per month.

## Testing Patterns

- **Test Framework:** Not explicitly detected; test files follow the `*.test.*` pattern.
- **Test File Naming:** Use `.test.` in filenames, e.g., `verseAnalyzer.test.ts`.
- **Typical Test Example:**
  ```typescript
  import { analyzeVerse } from './verseAnalyzer';

  describe('analyzeVerse', () => {
    it('should return correct analysis for a sample verse', () => {
      const result = analyzeVerse('Sample verse');
      expect(result).toHaveProperty('meaning');
    });
  });
  ```

## Commands

| Command                | Purpose                                                        |
|------------------------|----------------------------------------------------------------|
| /update-frontend-deps  | Update, fix, or synchronize frontend npm dependencies          |
```
