# ChatAI CLI

A powerful command-line interface for interacting with various AI models directly from your terminal.

## Features

- **Multiple AI Models**: Support for Llama, GPT, Qwen, Mistral, and other leading AI models
- **Chat Management**: Create and manage conversations with context preservation
- **Model Switching**: Dynamic model selection both through settings menu and direct commands
- **Export Functionality**: Save conversations in JSON or TXT formats
- **Usage Statistics**: Track token consumption and request metrics
- **Customizable System Messages**: Configure AI behavior through system prompts
- **Colored Interface**: Enhanced readability with color-coded output
- **Command System**: In-chat commands for enhanced control

## Commands

### Chat Commands
- `exit` - End current chat and return to main menu
- `status` - Display detailed token usage statistics
- `export json/txt` - Export conversation to specified format
- `model` - Show available models and interactively select one
- `model [number]` - Directly select model by its index
- `help` - Display command reference

### Settings Menu
- Model selection interface
- System message configuration

## Architecture

The application is structured around several key components:

- **API Client**: Handles communication with AI model endpoints
- **Model Management**: Loads, validates, and switches between different AI models
- **Database Layer**: SQLite-based storage for usage statistics
- **Export System**: Flexible conversation export in multiple formats
- **UI Components**: Terminal interface with color support and interactive menus

## Configuration

Models are defined in `config/models.json` with support for multiple providers. Application settings including default model and system messages are stored in `config/settings.json`.

## Data Management

Usage statistics are tracked in a SQLite database (`config/usage_stats.db`) with per-day and per-model metrics. Conversation history is maintained in memory during sessions and can be exported for persistence.

---

**ChatAI CLI** - Terminal-based AI interaction with enterprise-grade features.
