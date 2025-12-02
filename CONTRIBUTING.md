# Contributing to Delhivery Logistics Analysis Dashboard

First off, thank you for considering contributing to this project! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behavior includes:**
- Harassment or discriminatory language
- Trolling or insulting comments
- Public or private harassment
- Publishing others' private information

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)

**Bug Report Template:**
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Windows 10]
- Python Version: [e.g., 3.9.7]
- Streamlit Version: [e.g., 1.28.0]
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** for the enhancement
- **Proposed solution** or implementation
- **Alternative solutions** considered

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- Git
- Virtual environment tool (venv or conda)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Delhivery-Logistics-Analysis-Dashboard.git
cd Delhivery-Logistics-Analysis-Dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🔄 Pull Request Process

1. **Update Documentation**: Update README.md with details of changes if needed
2. **Follow Style Guidelines**: Ensure code follows PEP 8
3. **Test Your Changes**: Run the app and test all affected features
4. **Update Requirements**: Add any new dependencies to requirements.txt
5. **Clear Description**: Explain what and why in your PR description
6. **Link Issues**: Reference any related issues

### PR Checklist

- [ ] Code follows PEP 8 style guidelines
- [ ] Comments added for complex logic
- [ ] Documentation updated (if needed)
- [ ] All tests pass
- [ ] No new warnings introduced
- [ ] Screenshots included (for UI changes)

## 📝 Style Guidelines

### Python Code Style

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines:

```python
# Good
def calculate_delivery_time(distance, speed):
    """Calculate estimated delivery time.
    
    Args:
        distance (float): Distance in kilometers
        speed (float): Average speed in km/h
        
    Returns:
        float: Estimated time in hours
    """
    return distance / speed

# Bad
def calc(d,s):
    return d/s
```

### Streamlit Code Style

```python
# Good - Clear section headers
st.header("📊 Data Analysis")
st.subheader("Distribution Analysis")

# Good - Descriptive variable names
delivery_time_mean = df['actual_time'].mean()

# Good - Comments for complex logic
# Calculate IQR for outlier detection
Q1 = df['actual_time'].quantile(0.25)
Q3 = df['actual_time'].quantile(0.75)
IQR = Q3 - Q1
```

### Documentation Style

- Use clear, concise language
- Include code examples where helpful
- Add screenshots for UI features
- Keep formatting consistent

## 💬 Commit Message Guidelines

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding tests
- **chore**: Maintenance tasks

### Examples

```bash
# Good
feat(eda): add violin plots for distribution analysis

# Good
fix(hypothesis): correct p-value calculation for t-test

# Good
docs(readme): update installation instructions

# Bad
update stuff
fixed bug
changes
```

## 🎯 Areas for Contribution

### High Priority

- [ ] Add unit tests for data processing functions
- [ ] Implement data caching for better performance
- [ ] Add export to PDF functionality
- [ ] Create interactive tutorial/walkthrough

### Medium Priority

- [ ] Add more visualization types
- [ ] Implement user authentication
- [ ] Add database support
- [ ] Create API endpoints

### Low Priority

- [ ] Dark/light theme toggle
- [ ] Multi-language support
- [ ] Custom color schemes
- [ ] Advanced filtering options

## 📞 Questions?

Feel free to reach out:

- **Email**: rattudacsit2021gate@gmail.com
- **GitHub Issues**: [Create an issue](https://github.com/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard/issues)
- **LinkedIn**: [Ratnesh Kumar](https://www.linkedin.com/in/ratneshkumar1998/)

---

**Thank you for contributing! 🙏**
