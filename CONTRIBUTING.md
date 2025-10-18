# Contributing to BYU Major Advisor

Thank you for your interest in contributing to the BYU Major Advisor project! This guide will help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/Redo-Hackathon-2025.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## Development Setup

Follow the instructions in [QUICKSTART.md](QUICKSTART.md) to set up your development environment.

## Ways to Contribute

### 1. Add More Majors

The current database has 8 majors. Help expand it!

**How to add a major:**

1. Open `backend/data/majors.json`
2. Add a new entry following this structure:

```json
{
  "id": "major-id",
  "name": "Major Name",
  "college": "College Name at BYU",
  "description": "Brief description of the major",
  "interests": ["keyword1", "keyword2", "keyword3"],
  "prerequisites": ["Course1", "Course2"],
  "core_courses": ["Course3", "Course4", "Course5"],
  "total_credits": 120,
  "career_paths": ["Career1", "Career2", "Career3"],
  "average_salary": 70000,
  "first_year_courses": ["Course1", "Course2", "GE electives"]
}
```

**Tips:**
- Use BYU's official course catalog
- Include accurate salary data (use BLS.gov)
- Add relevant interest keywords for better matching
- Include common first-year courses

### 2. Improve the UI

**Areas that need work:**
- Mobile responsiveness
- Accessibility (ARIA labels, keyboard navigation)
- Animation and transitions
- Dark mode support
- Better error messaging

**UI Guidelines:**
- Follow BYU's brand colors
- Maintain consistent spacing
- Ensure readability
- Test on multiple browsers

### 3. Enhance the Chatbot

**Improvements needed:**
- Better conversation context
- Multi-turn conversations
- Understanding of follow-up questions
- More personalized responses
- Handling edge cases

### 4. Add Features

**Feature Ideas:**
- User authentication
- Save/load conversations
- Export schedules to PDF
- Compare 3+ majors side-by-side
- Course prerequisite graphs
- Integration with BYU's real course catalog
- Email schedule to student
- Advisor appointment booking

### 5. Write Tests

We need comprehensive testing!

**Test Coverage Needed:**
- Backend API endpoints
- Chatbot logic
- Schedule optimization
- Frontend components
- Integration tests
- E2E tests

**Example test structure:**

```python
# tests/test_chatbot.py
import unittest
from backend.utils.chatbot import MajorAdvisorChatbot

class TestChatbot(unittest.TestCase):
    def test_interest_analysis(self):
        # Test implementation
        pass
```

### 6. Documentation

**Documentation needs:**
- API endpoint examples
- Video tutorials
- User guide
- Deployment guide
- FAQ section

## Code Style Guidelines

### Python (Backend)

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions small and focused
- Handle errors gracefully

```python
def generate_schedule(major_ids: List[str], semester: str = "Fall") -> Dict[str, Any]:
    """
    Generate an optimized course schedule.
    
    Args:
        major_ids: List of major IDs to consider
        semester: Target semester (Fall/Winter)
        
    Returns:
        Dictionary with schedule and reasoning
    """
    # Implementation
```

### JavaScript/React (Frontend)

- Use functional components
- Follow React best practices
- Use descriptive component names
- Add prop validation
- Keep components focused

```javascript
const MajorCard = ({ major, onClick }) => {
  // Component implementation
};

export default MajorCard;
```

### CSS

- Use BYU brand colors
- Follow BEM naming convention
- Write mobile-first responsive styles
- Comment complex styles

```css
/* Component: Major Card */
.major-card {
  background: var(--white);
  border-radius: 12px;
}

.major-card__title {
  color: var(--byu-blue);
}
```

## Commit Message Guidelines

Write clear, descriptive commit messages:

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting)
- **refactor**: Code refactoring
- **test**: Adding tests
- **chore**: Maintenance tasks

**Examples:**
```
feat: Add schedule export to PDF
fix: Resolve schedule generation for 3+ majors
docs: Update API documentation with examples
style: Format code with black
refactor: Simplify chatbot interest matching
test: Add unit tests for schedule optimizer
chore: Update dependencies
```

## Pull Request Process

1. **Update documentation** if you changed APIs or added features
2. **Add tests** for new functionality
3. **Update README.md** if needed
4. **Ensure all tests pass**
5. **Follow the PR template**

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
How did you test these changes?

## Screenshots (if UI changes)
Add screenshots here

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
```

## Review Process

1. A maintainer will review your PR
2. Address any feedback
3. Once approved, your PR will be merged
4. Your contribution will be credited

## Questions?

- Open an issue for bugs
- Start a discussion for feature ideas
- Tag @AllyJoho for questions

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Enforcement

Unacceptable behavior may be reported to the project maintainers.

## Recognition

All contributors will be recognized in our README.md!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to BYU Major Advisor! 🎓
