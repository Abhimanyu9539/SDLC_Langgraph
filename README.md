# 🏗️ SDLC_Langgraph - AI-Powered Software Development Lifecycle Automation

A sophisticated LangGraph-based system that automates the early stages of software development using AI, featuring human-in-the-loop review capabilities and intelligent workflow orchestration.

## 🎯 Overview

SDLC_Langgraph transforms raw software requirements into structured user stories through an intelligent, multi-stage workflow. It leverages OpenAI's GPT models to enhance requirements, generate user stories, and facilitate product owner reviews with human oversight.

## ✨ Key Features

- 🤖 **AI-Powered Requirements Enhancement**: Automatically structures and validates raw requirements
- 📖 **Intelligent User Story Generation**: Creates INVEST-compliant user stories with acceptance criteria
- 🛑 **Human-in-the-Loop Reviews**: Proper LangGraph interrupt pattern for human oversight
- 🔄 **Iterative Improvement**: Revision cycles based on feedback
- 📊 **Visual Workflow**: Generate workflow graphs for documentation
- ⚙️ **Configurable Limits**: Adjustable story counts and iteration limits
- 🧵 **Thread-based State Management**: Maintains workflow state across interruptions

## 🏗️ Architecture

```
Requirements Input → User Story Generation → Product Owner Review → [Revision Loop] → Design Documents
```

### Core Components

- **Nodes**: Processing units for each workflow stage
- **State Management**: Thread-based state tracking with complete history
- **Workflow Engine**: LangGraph-powered orchestration
- **Review System**: Human/AI/Auto review modes
- **Visualization**: Workflow graph generation

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SDLC_Langgraph
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4
   TEMPERATURE=0.3
   MAX_TOKENS=4096
   MAX_ITERATIONS=3
   MAX_USER_STORIES=3
   ENABLE_LOGGING=true
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## 📋 Usage

### Interactive Mode

The application provides an interactive menu:

```
🏗️ PROPER LANGGRAPH INTERRUPT WORKFLOW
======================================
1. 🚀 Run Workflow (Proper Interrupts)
2. 🔄 Display Workflow Graph
3. 📊 Show Implementation Status
4. 🧪 Debug Workflow State
5. ❌ Exit
```

### Workflow Execution

1. **Select Option 1** to run the workflow
2. **Enter your project requirements** when prompted
3. **Choose review method** when workflow pauses:
   - **Human**: Manual review with your input
   - **AI**: Automated review using GPT
   - **Auto**: Instant approval
4. **Review generated user stories** and provide feedback
5. **Iterate** if revisions are needed

### Example Requirements Input

```
Build a task management application with user authentication, 
project creation, task assignment, and progress tracking. 
Include role-based access control and real-time notifications.
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4.1-nano` | OpenAI model to use |
| `TEMPERATURE` | `0.3` | AI response creativity (0-1) |
| `MAX_TOKENS` | `4096` | Maximum tokens per response |
| `MAX_ITERATIONS` | `3` | Maximum revision cycles |
| `MAX_USER_STORIES` | `3` | Maximum stories to generate |
| `ENABLE_LOGGING` | `true` | Enable detailed logging |

### Customization

Modify `config/settings.py` to adjust default values or add new configuration options.

## 📁 Project Structure

```
SDLC_Langgraph/
├── main.py                          # Main application entry point
├── config/
│   └── settings.py                  # Configuration management
├── state/
│   └── sdlc_state.py               # Data structure definitions
├── nodes/                          # Workflow processing nodes
│   ├── requirements_node.py        # Requirements capture & enhancement
│   ├── user_stories_node.py        # User story generation
│   ├── product_owner_review_node.py # Review & approval logic
│   └── enhanced_product_owner_review_node.py # Advanced review features
├── workflow/                       # Workflow definitions
│   ├── sdlc_workflow.py           # Basic workflow
│   └── proper_interrupt_workflow.py # Advanced interrupt workflow
├── utils/                         # Helper utilities
│   ├── proper_workflow_runner.py  # Workflow execution engine
│   ├── llm_utils.py              # OpenAI integration
│   ├── visualization_utils.py    # Graph visualization
│   └── simple_review_handler.py  # Review choice handling
└── workflow_graph.png            # Visual workflow representation
```

## 🔄 Workflow Stages

### 1. Requirements Capture
- **Node**: `ui_user_inputs_requirements`
- **Function**: Enhances and validates raw requirements
- **Output**: Structured requirements document

### 2. User Story Generation
- **Node**: `auto_generate_user_stories`
- **Function**: Creates INVEST-compliant user stories
- **Output**: Prioritized user stories with acceptance criteria

### 3. Product Owner Review ⚡
- **Node**: `product_owner_review`
- **Function**: Review and approval process
- **Interrupt Point**: Human-in-the-loop decision making

### 4. Conditional Routing
- **Node**: `route_after_po_review`
- **Function**: Routes based on approval status
- **Paths**: Approved → Design, Needs Revision → Revision Loop

### 5. Revision Loop
- **Node**: `revise_user_stories`
- **Function**: AI-powered story revision
- **Flow**: Returns to review stage

## 🎛️ Review Modes

### Human Review
- Manual review with user input
- Detailed feedback collection
- Iterative improvement cycles

### AI Review
- Automated review using GPT
- Consistent evaluation criteria
- Quick feedback generation

### Auto Review
- Instant approval
- Bypass review process
- Suitable for simple requirements

## 🛠️ Development

### Adding New Nodes

1. Create a new file in `nodes/`
2. Define your node function with proper state handling
3. Add the node to the workflow in `workflow/sdlc_workflow.py`
4. Update state definitions if needed

### Extending State

1. Modify `state/sdlc_state.py`
2. Add new fields to `SDLCState` TypedDict
3. Update node functions to handle new state fields

### Custom Workflows

1. Create new workflow file in `workflow/`
2. Define node connections and conditional edges
3. Implement proper interrupt patterns if needed

## 🧪 Testing

### Debug Mode

Use the debug option in the main menu to inspect workflow state:

```
4. 🧪 Debug Workflow State
```

### State Inspection

The system provides detailed state information including:
- Current stage
- User stories generated
- Review history
- Iteration count
- Approval status

## 📊 Output Examples

### Generated User Stories

```
📖 Generated User Stories:

1. US-001: User Authentication
   🎯 Priority: High | 📊 Points: 8
   📝 As an end user, I want to securely log into the system so that I can access my personal dashboard
   ✅ 2 acceptance criteria defined

2. US-002: Dashboard View
   🎯 Priority: High | 📊 Points: 5
   📝 As an authenticated user, I want to view my dashboard so that I can see my key information
   ✅ 2 acceptance criteria defined
```

### Review History

```
📚 COMPLETE REVIEW HISTORY (2 reviews):

   📋 Review 1 (Iteration 0):
      👤 Reviewer: AI
      ✅ Status: APPROVED
      💬 Feedback: Stories are well-structured and cover core functionality...

   📋 Review 2 (Iteration 1):
      👤 Reviewer: Human
      ✅ Status: APPROVED
      💬 Feedback: Excellent user stories with clear acceptance criteria...
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 References

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Human-in-the-Loop Workflows](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## 🆘 Support

For issues and questions:
1. Check the debug mode for state information
2. Review the workflow graph visualization
3. Examine the implementation status
4. Create an issue with detailed error information

---

**Built with ❤️ using LangGraph and OpenAI**