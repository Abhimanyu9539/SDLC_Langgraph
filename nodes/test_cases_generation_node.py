# ==================== TEST CASES GENERATION NODE ====================
# File: nodes/test_cases_generation_node.py

from datetime import datetime
from typing import List, Dict, Any
from state.sdlc_state import SDLCState
from utils.llm_utils import LLMUtils
from config.settings import settings
import traceback

def generate_test_cases(state: SDLCState) -> SDLCState:
    """
    Generate Test Cases based on code, user stories, and acceptance criteria
    
    This node:
    1. Analyzes the generated Python code
    2. Extracts user stories and acceptance criteria
    3. Generates comprehensive unit tests
    4. Creates test scenarios for edge cases
    5. Generates test data and fixtures
    """
    
    print("\n🧪 Generating Test Cases")
    print("🎯 Creating comprehensive unit tests and test scenarios")
    
    code_files = state.get("code", {})
    user_stories = state.get("user_stories", [])
    design_docs = state.get("design_docs", {})
    
    # Debug information
    print(f"🔍 DEBUG: Code files available: {bool(code_files)}")
    print(f"🔍 DEBUG: Code files: {list(code_files.keys())}")
    print(f"🔍 DEBUG: User stories count: {len(user_stories)}")
    
    if not code_files:
        print("⚠️ No code files found - cannot generate test cases")
        return {
            **state,
            "current_stage": "test_generation_failed",
            "timestamp": datetime.now().isoformat()
        }
    
    print(f"🧪 Generating test cases for {len(code_files)} code files...")
    
    # Generate comprehensive test cases
    test_cases = _generate_comprehensive_test_cases(code_files, user_stories, design_docs)
    
    # Debug the results
    print(f"🔍 DEBUG: Generated {len(test_cases)} test files")
    print(f"🔍 DEBUG: Test file names: {list(test_cases.keys())}")
    
    # Update state with generated test cases
    updated_state = {
        **state,
        "test_cases": test_cases,
        "current_stage": "test_cases_generated",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"✅ Test cases generated successfully")
    print(f"📄 Generated {len(test_cases)} test files")
    
    return updated_state

def _generate_comprehensive_test_cases(code_files: Dict[str, str], user_stories: List[Dict[str, Any]], design_docs: Dict[str, Any]) -> Dict[str, str]:
    """Generate comprehensive test cases using LLM"""
    
    llm_utils = LLMUtils()
    
    # Extract test requirements
    test_requirements = _extract_test_requirements(user_stories, design_docs)
    
    # Analyze code structure for better test generation
    code_analysis = _analyze_code_structure(code_files)
    
    # System prompt for test generation
    system_prompt = """
    You are a Senior QA Engineer and Test Automation Expert. Generate comprehensive test cases for the provided Python code.
    
    TESTING REQUIREMENTS:
    1. Generate unit tests using pytest framework
    2. Create test cases for all functions and classes
    3. Test both positive and negative scenarios
    4. Include edge cases and boundary conditions
    5. Test error handling and exception cases
    6. Create integration tests for user story scenarios
    7. Generate test data and fixtures
    8. Include performance and load testing scenarios
    9. Test input validation and security aspects
    10. Ensure high test coverage
    
    TEST STRUCTURE:
    - Use pytest as the testing framework
    - Follow naming convention: test_*.py
    - Include proper test documentation
    - Use fixtures for test data setup
    - Include setup and teardown methods
    - Add parametrized tests for multiple scenarios
    - Include mocking where appropriate
    
    TESTING BEST PRACTICES:
    - Follow AAA pattern (Arrange, Act, Assert)
    - Write clear, descriptive test names
    - Include test docstrings explaining purpose
    - Test one concept per test function
    - Use appropriate assertion methods
    - Include both unit and integration tests
    - Test error conditions and edge cases
    
    RESPONSE FORMAT:
    Generate complete, executable test files.
    Return ONLY the Python test code, no explanations or markdown formatting.
    Focus on creating practical, comprehensive test coverage.
    """
    
    user_prompt = f"""
    Generate comprehensive test cases for this Python application:
    
    CODE TO TEST:
    {_format_code_for_testing(code_files)}
    
    USER STORY REQUIREMENTS:
    {test_requirements}
    
    CODE ANALYSIS:
    {code_analysis}
    
    Create a complete test suite that validates:
    1. All functions work correctly with valid inputs
    2. Error handling for invalid inputs
    3. Edge cases and boundary conditions
    4. User story acceptance criteria
    5. Integration scenarios
    6. Performance considerations
    
    Generate thorough test cases that ensure code quality and reliability.
    """
    
    try:
        print("🤖 Generating test cases using AI...")
        print(f"🔍 DEBUG: System prompt length: {len(system_prompt)}")
        print(f"🔍 DEBUG: User prompt length: {len(user_prompt)}")
        
        # Use get_completion for test generation
        test_code = llm_utils.get_completion(system_prompt, user_prompt)
        
        # Clean up the response
        test_code = _clean_test_code_response(test_code)
        
        # Create test files dictionary
        test_cases = {
            "test_main.py": test_code
        }
        
        print(f"✅ Test cases generated successfully")
        print(f"📏 Generated test code length: {len(test_code)} characters")
        
        # Validate that we got meaningful test code
        if len(test_code.strip()) < 100 or "def test_" not in test_code:
            print("⚠️ Generated test code seems insufficient, using enhanced fallback")
            return _generate_fallback_test_cases(code_files, user_stories)
        
        return test_cases
        
    except Exception as e:
        print(f"❌ Error generating test cases: {e}")
        print(f"❌ Error type: {type(e)}")
        print(f"❌ Full traceback: {traceback.format_exc()}")
        
        print("🔄 Using fallback test case generation...")
        return _generate_fallback_test_cases(code_files, user_stories)

def _extract_test_requirements(user_stories: List[Dict[str, Any]], design_docs: Dict[str, Any]) -> str:
    """Extract testing requirements from user stories and design documents"""
    
    requirements = []
    
    # Extract from user stories
    if user_stories:
        requirements.append("USER STORY TEST REQUIREMENTS:")
        
        for i, story in enumerate(user_stories, 1):
            story_id = story.get('id', f'US-{i}')
            title = story.get('title', 'Feature')
            description = story.get('description', '')
            
            requirements.append(f"\n{i}. {story_id}: {title}")
            requirements.append(f"   Description: {description}")
            
            # Add acceptance criteria as test scenarios
            criteria = story.get('acceptance_criteria', [])
            if criteria:
                requirements.append("   Test Scenarios:")
                for j, criterion in enumerate(criteria, 1):
                    requirements.append(f"      {j}. {criterion}")
            
            # Add business value context
            business_value = story.get('business_value', '')
            if business_value:
                requirements.append(f"   Business Value: {business_value}")
    
    # Extract from design documents
    if design_docs:
        requirements.append("\n\nDESIGN-BASED TEST REQUIREMENTS:")
        
        # System architecture testing
        sys_arch = design_docs.get('system_architecture', {})
        if sys_arch:
            components = sys_arch.get('components', [])
            if components:
                requirements.append(f"Components to test: {', '.join(components)}")
        
        # Database testing
        db_design = design_docs.get('database_design', {})
        if db_design:
            entities = db_design.get('entities', [])
            if entities:
                requirements.append(f"Data entities to test: {', '.join(entities)}")
        
        # API testing
        api_design = design_docs.get('api_design', {})
        if api_design:
            endpoints = api_design.get('core_endpoints', [])
            if endpoints:
                requirements.append(f"API endpoints to test: {', '.join(endpoints)}")
    
    if not requirements:
        return "Generate comprehensive unit tests for all functions and classes in the code."
    
    return "\n".join(requirements)

def _analyze_code_structure(code_files: Dict[str, str]) -> str:
    """Analyze code structure to better inform test generation"""
    
    analysis = []
    
    for filename, content in code_files.items():
        analysis.append(f"\nFILE: {filename}")
        
        # Count functions and classes
        functions = []
        classes = []
        imports = []
        
        lines = content.split('\n')
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('def ') and '(' in stripped:
                func_name = stripped.split('(')[0].replace('def ', '').strip()
                functions.append(func_name)
            
            elif stripped.startswith('class ') and ':' in stripped:
                class_name = stripped.split(':')[0].replace('class ', '').strip()
                if '(' in class_name:
                    class_name = class_name.split('(')[0]
                classes.append(class_name)
            
            elif stripped.startswith('import ') or stripped.startswith('from '):
                imports.append(stripped)
        
        # Add analysis results
        if functions:
            analysis.append(f"Functions to test: {', '.join(functions)}")
        if classes:
            analysis.append(f"Classes to test: {', '.join(classes)}")
        if imports:
            analysis.append(f"Dependencies: {len(imports)} imports found")
        
        # Analyze complexity indicators
        complexity_indicators = []
        if 'if ' in content:
            complexity_indicators.append("conditional logic")
        if 'for ' in content or 'while ' in content:
            complexity_indicators.append("loops")
        if 'try:' in content:
            complexity_indicators.append("exception handling")
        if 'input(' in content:
            complexity_indicators.append("user input")
        if 'open(' in content:
            complexity_indicators.append("file operations")
        
        if complexity_indicators:
            analysis.append(f"Test focus areas: {', '.join(complexity_indicators)}")
    
    return "\n".join(analysis) if analysis else "Basic Python application structure detected."

def _format_code_for_testing(code_files: Dict[str, str]) -> str:
    """Format code files for test generation"""
    
    formatted_code = []
    
    for filename, content in code_files.items():
        formatted_code.append(f"=== {filename} ===")
        formatted_code.append(content)
        formatted_code.append("")  # Empty line separator
    
    return "\n".join(formatted_code)

def _clean_test_code_response(response: str) -> str:
    """Clean up LLM response to extract just the test code"""
    
    # Remove markdown code blocks if present
    if "```python" in response:
        # Extract content between ```python and ```
        start_marker = "```python"
        end_marker = "```"
        
        start_idx = response.find(start_marker)
        if start_idx != -1:
            start_idx += len(start_marker)
            end_idx = response.find(end_marker, start_idx)
            if end_idx != -1:
                response = response[start_idx:end_idx].strip()
    
    elif "```" in response:
        # Extract content between ``` blocks
        parts = response.split("```")
        if len(parts) >= 3:
            response = parts[1].strip()
    
    # Remove any leading/trailing whitespace
    response = response.strip()
    
    return response

def _generate_fallback_test_cases(code_files: Dict[str, str], user_stories: List[Dict[str, Any]]) -> Dict[str, str]:
    """Generate basic fallback test cases when AI generation fails"""
    
    main_code_file = list(code_files.keys())[0] if code_files else "main.py"
    main_code_content = list(code_files.values())[0] if code_files else ""
    
    # Extract function names for basic test generation
    functions = []
    classes = []
    
    if main_code_content:
        lines = main_code_content.split('\n')
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('def ') and '(' in stripped:
                func_name = stripped.split('(')[0].replace('def ', '').strip()
                if not func_name.startswith('_'):  # Skip private functions
                    functions.append(func_name)
            elif stripped.startswith('class ') and ':' in stripped:
                class_name = stripped.split(':')[0].replace('class ', '').strip()
                if '(' in class_name:
                    class_name = class_name.split('(')[0]
                classes.append(class_name)
    
    # Generate basic test structure
    fallback_test = f'''#!/usr/bin/env python3
"""
Generated Test Cases - Fallback Implementation

This is a basic test suite created when the main test generation
process encountered issues.

Please review and enhance these tests based on your requirements.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add the source directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main application
try:
    from main import *
except ImportError:
    print("Warning: Could not import main module. Please adjust imports as needed.")

class TestBasicFunctionality:
    """Basic functionality tests"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.test_data = {{"id": 1, "name": "Test Data"}}
    
    def teardown_method(self):
        """Cleanup after each test method"""
        pass
'''

    # Add function tests
    if functions:
        fallback_test += f'''
    # Generated tests for detected functions
'''
        for func in functions[:5]:  # Limit to first 5 functions
            fallback_test += f'''
    def test_{func}_valid_input(self):
        """Test {func} with valid input"""
        # TODO: Implement test for {func}
        # Example test structure:
        # result = {func}(valid_input)
        # assert result is not None
        # assert expected_condition
        pass
    
    def test_{func}_invalid_input(self):
        """Test {func} with invalid input"""
        # TODO: Implement error case test for {func}
        # Example test structure:
        # with pytest.raises(ExpectedException):
        #     {func}(invalid_input)
        pass
'''

    # Add class tests
    if classes:
        fallback_test += f'''
class TestClasses:
    """Tests for application classes"""
'''
        for cls in classes[:3]:  # Limit to first 3 classes
            fallback_test += f'''
    def test_{cls.lower()}_initialization(self):
        """Test {cls} initialization"""
        # TODO: Implement {cls} initialization test
        # Example test structure:
        # instance = {cls}()
        # assert instance is not None
        # assert instance has expected properties
        pass
    
    def test_{cls.lower()}_methods(self):
        """Test {cls} methods"""
        # TODO: Implement {cls} method tests
        # Example test structure:
        # instance = {cls}()
        # result = instance.method_name()
        # assert result meets expectations
        pass
'''

    # Add user story tests
    if user_stories:
        fallback_test += f'''
class TestUserStories:
    """Tests based on user stories and acceptance criteria"""
'''
        for i, story in enumerate(user_stories[:3], 1):  # Limit to first 3 stories
            story_id = story.get('id', f'US-{i}')
            title = story.get('title', 'Feature').replace(' ', '_').lower()
            
            fallback_test += f'''
    def test_{story_id.lower().replace('-', '_')}_{title}(self):
        """Test user story: {story.get('title', 'Feature')}"""
        # User Story: {story.get('description', 'No description')}
        # TODO: Implement test for user story acceptance criteria
        
        # Acceptance Criteria to test:
'''
            criteria = story.get('acceptance_criteria', [])
            for j, criterion in enumerate(criteria[:3], 1):  # Limit to first 3 criteria
                fallback_test += f'''        # {j}. {criterion}
'''
            
            fallback_test += f'''        
        # Example test implementation:
        # 1. Setup test conditions
        # 2. Execute the feature
        # 3. Verify acceptance criteria
        pass
'''

    # Add integration tests
    fallback_test += f'''
class TestIntegration:
    """Integration tests for end-to-end scenarios"""
    
    def test_application_startup(self):
        """Test that the application starts correctly"""
        # TODO: Test application initialization
        # Example: Verify main components load properly
        pass
    
    def test_main_workflow(self):
        """Test the main application workflow"""
        # TODO: Test end-to-end application flow
        # Example: Simulate user interaction and verify results
        pass
    
    @pytest.mark.parametrize("test_input,expected", [
        ("valid_input", "expected_output"),
        ("edge_case", "edge_result"),
    ])
    def test_parametrized_scenarios(self, test_input, expected):
        """Test multiple scenarios with different inputs"""
        # TODO: Implement parametrized tests
        # result = your_function(test_input)
        # assert result == expected
        pass

class TestErrorHandling:
    """Tests for error handling and edge cases"""
    
    def test_invalid_input_handling(self):
        """Test application handles invalid input gracefully"""
        # TODO: Test error handling for various invalid inputs
        pass
    
    def test_exception_scenarios(self):
        """Test exception handling in critical functions"""
        # TODO: Test that exceptions are properly handled
        pass

# Test fixtures
@pytest.fixture
def sample_data():
    """Provide sample test data"""
    return {{
        "test_user": {{"id": 1, "name": "Test User"}},
        "test_data": {{"value": "test_value"}},
        "test_list": [1, 2, 3, 4, 5]
    }}

@pytest.fixture
def mock_database():
    """Mock database for testing"""
    return Mock()

# Helper functions for tests
def assert_valid_response(response):
    """Helper function to validate response format"""
    assert response is not None
    # Add more validation as needed

if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__])
'''
    
    return {"test_main.py": fallback_test}