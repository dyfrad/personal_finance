# ADR 004: Testing Architecture and Quality Assurance

## Status
Accepted

## Context
The personal finance application handles sensitive financial data and complex calculations that require high reliability. Users depend on accurate portfolio tracking, and system failures could result in data loss or incorrect financial information. A comprehensive testing strategy is essential to ensure:

1. **Data Integrity**: All financial calculations are accurate
2. **System Reliability**: The application handles errors gracefully without crashing
3. **Performance**: The system works with realistic portfolio sizes
4. **Regression Prevention**: New changes don't break existing functionality
5. **Database Consistency**: Data remains consistent across all operations

## Decision
We will implement a comprehensive, multi-layered testing architecture with **33 focused tests** covering critical functionality rather than attempting exhaustive coverage of every feature.

### Testing Strategy
**Focus on Critical Paths**: Test the functionality that users depend on most heavily and that could cause the most damage if it fails.

### Test Structure
```
tests/
├── test_app_critical.py       # Critical application functionality (13 tests)
├── test_database.py           # Database operations (9 tests)  
├── test_models.py             # Data models (11 tests)
├── conftest.py                # Test configuration and fixtures
└── TEST_COVERAGE_SUMMARY.md   # Documentation of test coverage
```

### Test Categories

#### 1. Critical Application Functionality (13 tests)
**Purpose**: Test the core operations that users depend on daily

**Coverage**:
- **Database Operations**: Item insertion, retrieval, deletion with integrity
- **Purchase System**: Investment purchase tracking and calculations  
- **Data Persistence**: Different item types (investments, inventory, expenses)
- **Error Handling**: Corrupted databases, invalid queries
- **Business Logic**: Investment calculations, inventory handling, expense tracking
- **Data Integrity**: ID uniqueness, consistency after operations
- **System Limits**: Large portfolios (50+ items), high transaction volumes (20+ purchases)

#### 2. Database Layer (9 tests)
**Purpose**: Validate low-level database operations and error handling

**Coverage**:
- Database initialization and schema creation
- CRUD operations (Create, Read, Update, Delete)
- Purchase management and foreign key relationships
- Data clearing and bulk operations
- Connection error handling
- Query error protection

#### 3. Data Models (11 tests) 
**Purpose**: Ensure business object integrity and calculations

**Coverage**:
- Item model creation and property management
- Purchase tracking and aggregation
- Financial calculations (total invested, current value, profit/loss)
- Data serialization (to/from dictionaries)
- Purchase model functionality

### Testing Principles

#### Real-World Scenarios
- **Realistic Portfolio Sizes**: Test with 50+ items (typical user portfolio)
- **Active Trading**: Test items with 20+ purchases (heavy trading scenarios)
- **Mixed Portfolios**: Combinations of investments, inventory, and expenses
- **Edge Cases**: Empty portfolios, single transactions, maximum values

#### Error Resilience
- **Database Corruption**: Handle corrupted SQLite files gracefully
- **Invalid Data**: Protect against malformed input
- **Network Issues**: Handle missing stock data without crashing
- **Resource Constraints**: Test behavior under memory/disk pressure

#### Financial Accuracy
- **Multi-Purchase Calculations**: Complex investment scenarios with multiple buy orders
- **Category-Specific Logic**: Different calculation rules for investments vs. inventory
- **Precision Testing**: Ensure financial calculations are accurate to cents
- **Boundary Testing**: Test with zero values, negative amounts, extreme numbers

## Consequences

### Positive
- **High Confidence**: 33/33 tests passing provides confidence in core functionality
- **Fast Feedback**: Focused test suite runs quickly (< 2 seconds)
- **Clear Coverage**: Each test has a specific, documented purpose
- **Regression Prevention**: Changes are validated against critical functionality
- **Documentation**: Tests serve as living documentation of expected behavior
- **Quality Assurance**: Systematic validation of financial calculations

### Negative
- **Limited Coverage**: Not every feature is tested (GUI, advanced analytics)
- **Maintenance Overhead**: Tests must be updated as functionality changes
- **False Confidence**: Passing tests don't guarantee zero bugs
- **Test Data Management**: Requires careful fixture management

### Neutral
- **Test Performance**: Small, focused test suite is fast and reliable
- **Code Complexity**: Tests add to codebase but improve maintainability

## Implementation Details

### Test Infrastructure
```python
# Test fixtures for database isolation
@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    fd, path = tempfile.mkstemp()
    os.close(fd)
    db = Database(db_name=path)
    yield db
    os.unlink(path)

# Sample data fixtures
@pytest.fixture
def sample_item():
    """Create a sample item for testing"""
    return Item("Test Stock", "Stocks", 100.0, "2024-01-01", 150.0, 50.0)
```

### Test Execution
```bash
# Run all tests
python -m pytest tests/ -v

# Quick validation
python -m pytest tests/ -q

# Specific test categories
python -m pytest tests/test_app_critical.py -v
```

### Quality Metrics
- **Success Rate**: 100% (33/33 tests passing)
- **Execution Time**: < 2 seconds for full suite
- **Coverage Focus**: Critical user journeys and data integrity
- **Error Scenarios**: Database corruption, invalid data, system limits
- **Protection Validation**: Database protection framework automatically safeguards test data

### Test Design Patterns

#### Isolated Testing
Each test uses temporary databases to ensure complete isolation and prevent test interference.

#### Realistic Data
Tests use realistic financial data and scenarios rather than trivial examples.

#### Comprehensive Validation
Tests verify not just that operations succeed, but that they produce correct results.

#### Error Path Testing
Explicit testing of error conditions and edge cases.

## Validation Approach

### Manual Testing Integration
Automated tests are complemented by:
- Manual GUI testing for user experience validation
- Performance testing with real user data
- Integration testing with external services (stock data)

### Continuous Validation
- All tests run on every code change
- New features require corresponding tests
- Refactoring must maintain test success

## Related Decisions
- ADR 001: Flexible Item Model - Tests validate the item model implementation
- ADR 002: Database Schema - Tests ensure schema integrity and operations
- ADR 003: GUI Design - Future: GUI testing considerations
- ADR 005: Database Protection Framework - Testing validates protection mechanisms

## Future Considerations
- **GUI Testing**: Framework for automated GUI testing
- **Performance Benchmarks**: Formal performance testing with metrics
- **Integration Testing**: Testing with real stock data APIs
- **Load Testing**: Testing with very large portfolios (1000+ items)
- **Security Testing**: Input validation and SQL injection prevention 