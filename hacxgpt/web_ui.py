"""
HacxGPT Web UI - Gradio Interface
Terminal-themed ChatGPT-like interface with hacker aesthetics
"""

import gradio as gr
import os
import time
from typing import List, Tuple, Optional
from .config import Config
from .core.brain import HacxBrain
from .core.extractor import CodeExtractor


class HacxWebUI:
    """Web-based UI for HacxGPT using Gradio"""
    
    def __init__(self):
        self.brain: Optional[HacxBrain] = None
        self.current_provider = None
        self.current_model = None
        self.conversation_history = []
        
    def initialize_brain(self, provider: str, api_key: str, model: str) -> Tuple[str, bool]:
        """Initialize the AI brain with given credentials"""
        try:
            Config.initialize()
            Config.ACTIVE_PROVIDER = provider
            Config.ACTIVE_MODEL = model
            
            self.brain = HacxBrain(api_key)
            self.current_provider = provider
            self.current_model = model
            
            return f"✓ Neural link established with {provider.upper()} | Model: {model}", True
        except Exception as e:
            return f"✗ Connection failed: {str(e)}", False
    
    def chat(self, message: str, history: List) -> Tuple[List, str]:
        """Process chat message and return updated history (Gradio 6.x format)"""
        if not self.brain:
            # Gradio 6.x format: list of dicts with 'role' and 'content'
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": "⚠️ **Error**: Neural link not established. Please configure API settings first."})
            return history, ""
        
        if not message.strip():
            return history, ""
        
        # Handle commands
        if message.startswith('/'):
            response = self._handle_command(message)
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response})
            return history, ""
        
        # Add user message to history
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": ""})
        
        # Stream response
        full_response = ""
        try:
            generator = self.brain.chat(message)
            for chunk in generator:
                if chunk:
                    full_response += chunk
                    # Update the last message in history with streaming response
                    history[-1]["content"] = full_response
                    yield history, ""
        except Exception as e:
            history[-1]["content"] = f"⚠️ **Error**: {str(e)}"
            yield history, ""
        
        return history, ""
    
    def _handle_command(self, command: str) -> str:
        """Handle special commands"""
        cmd = command.lower().strip()
        
        if cmd == '/help':
            return """**Available Commands:**
- `/help` - Show this help message
- `/status` - Show current configuration
- `/models` - List available models
- `/clear` - Clear conversation history
- `/new` - Start new conversation (reset memory)
"""
        
        elif cmd == '/status':
            if not self.brain:
                return "⚠️ No active connection"
            return f"""**System Status:**
- **Provider**: {self.current_provider.upper()}
- **Model**: {self.current_model}
- **Status**: ✓ Connected
"""
        
        elif cmd == '/models':
            if not self.current_provider:
                return "⚠️ No provider selected"
            models = Config.get_provider_config(self.current_provider).get("models", [])
            model_list = "\n".join([f"- `{m['name']}` - {m['alias']}" for m in models])
            return f"**Available Models for {self.current_provider.upper()}:**\n{model_list}"
        
        elif cmd == '/clear':
            return "✓ Use the 'Clear' button to clear conversation history"
        
        elif cmd == '/new':
            if self.brain:
                self.brain.reset()
                return "✓ Memory wiped. New session started."
            return "⚠️ No active connection"
        
        else:
            return f"⚠️ Unknown command: {command}\nType `/help` for available commands"
    
    def clear_history(self):
        """Clear conversation history"""
        if self.brain:
            self.brain.reset()
        return []
    
    def change_provider(self, provider: str, api_key: str, model: str) -> str:
        """Change provider and reinitialize"""
        if not api_key.strip():
            return "⚠️ API key required"
        
        status, success = self.initialize_brain(provider, api_key, model)
        return status
    
    def get_models_for_provider(self, provider: str) -> gr.Dropdown:
        """Get available models for selected provider"""
        Config.load_providers()
        models = Config.get_provider_config(provider).get("models", [])
        model_choices = [m["name"] for m in models]
        default_model = Config.get_provider_config(provider).get("default_model")
        
        return gr.Dropdown(
            choices=model_choices,
            value=default_model,
            label="Model"
        )


def create_ui():
    """Create and configure the Gradio interface"""
    
    ui_instance = HacxWebUI()
    
    # Minimal CSS - Simple and clean like ChatGPT
    custom_css = """
    /* Main theme colors */
    :root {
        --primary-color: #00ff41;
        --secondary-color: #00d4ff;
        --bg-dark: #0a0e27;
        --bg-darker: #050810;
        --text-color: #e8e8e8;
        --border-color: #00ff4150;
        --code-bg: #1e1e1e;
    }
    
    /* Dark background */
    body, .gradio-container {
        background: linear-gradient(135deg, #0a0e27 0%, #050810 100%) !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif !important;
    }
    
    /* Chat container - simple */
    .chatbot {
        background: rgba(10, 14, 39, 0.8) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    /* Messages - clean and simple */
    .message {
        padding: 16px !important;
        margin: 8px 0 !important;
        border-radius: 8px !important;
        line-height: 1.6 !important;
    }
    
    .message.user {
        background: rgba(26, 31, 58, 0.6) !important;
        border-left: 3px solid var(--secondary-color) !important;
        color: #e8e8e8 !important;
    }
    
    .message.bot {
        background: rgba(15, 20, 37, 0.6) !important;
        border-left: 3px solid var(--primary-color) !important;
        color: #e8e8e8 !important;
    }
    
    /* Code blocks - simple, clean, copyable */
    pre {
        background: var(--code-bg) !important;
        border: 1px solid #333 !important;
        border-radius: 6px !important;
        padding: 16px !important;
        margin: 12px 0 !important;
        overflow-x: auto !important;
        font-family: 'Courier New', 'Consolas', monospace !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
    }
    
    code {
        background: var(--code-bg) !important;
        color: #e8e8e8 !important;
        padding: 2px 6px !important;
        border-radius: 3px !important;
        font-family: 'Courier New', 'Consolas', monospace !important;
        font-size: 14px !important;
    }
    
    pre code {
        background: transparent !important;
        padding: 0 !important;
        color: #e8e8e8 !important;
        display: block !important;
        white-space: pre !important;
    }
    
    /* Remove syntax highlighting colors that interfere with copying */
    .token, .keyword, .string, .comment, .function, .operator {
        color: inherit !important;
        background: transparent !important;
    }
    
    /* Input field */
    .input-text, textarea {
        background: rgba(10, 14, 39, 0.9) !important;
        border: 2px solid var(--border-color) !important;
        color: var(--text-color) !important;
        border-radius: 8px !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    .input-text:focus, textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.3) !important;
    }
    
    /* Buttons */
    .btn, button {
        background: linear-gradient(135deg, #1a1f3a 0%, #0f1425 100%) !important;
        border: 2px solid var(--primary-color) !important;
        color: var(--primary-color) !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        transition: all 0.3s ease !important;
    }
    
    .btn:hover, button:hover {
        background: var(--primary-color) !important;
        color: var(--bg-dark) !important;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.5) !important;
    }
    
    /* Dropdown and select */
    select, .dropdown {
        background: rgba(10, 14, 39, 0.9) !important;
        border: 2px solid var(--border-color) !important;
        color: var(--text-color) !important;
        border-radius: 6px !important;
    }
    
    /* Labels */
    label {
        color: var(--primary-color) !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    /* Accordion */
    .accordion {
        background: rgba(10, 14, 39, 0.8) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--primary-color) !important;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.5) !important;
    }
    
    /* Links */
    a {
        color: var(--secondary-color) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        background: var(--bg-darker);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }
    """
    
    with gr.Blocks(title="HacxGPT - Neural Interface") as interface:
        
        # Header
        gr.Markdown("""
        # 🔥 HACXGPT - NEURAL INTERFACE
        ### SYSTEM: UNRESTRICTED | PROTOCOL: ACTIVE
        > Advanced AI Terminal Interface - Web Edition
        """)
        
        with gr.Row():
            with gr.Column(scale=4):
                # Main chat interface
                chatbot = gr.Chatbot(
                    label="Neural Link Console",
                    height=600,
                    show_label=True,
                    avatar_images=(None, "🤖")
                )
                
                with gr.Row():
                    msg_input = gr.Textbox(
                        label="Command Input",
                        placeholder="Enter your message or command (type /help for commands)...",
                        lines=2,
                        max_lines=10,
                        show_label=False,
                        scale=9
                    )
                    submit_btn = gr.Button("⚡ SEND", scale=1, variant="primary")
                
                with gr.Row():
                    clear_btn = gr.Button("🗑️ Clear", size="sm")
                    new_session_btn = gr.Button("🔄 New Session", size="sm")
                    help_btn = gr.Button("❓ Help", size="sm")
            
            with gr.Column(scale=1):
                # Configuration panel
                with gr.Accordion("⚙️ SYSTEM CONFIG", open=True):
                    status_display = gr.Textbox(
                        label="Status",
                        value="⚠️ Not Connected",
                        interactive=False,
                        lines=2
                    )
                    
                    provider_dropdown = gr.Dropdown(
                        choices=list(Config.PROVIDERS.keys()),
                        value=list(Config.PROVIDERS.keys())[0] if Config.PROVIDERS else None,
                        label="Provider",
                        interactive=True
                    )
                    
                    model_dropdown = gr.Dropdown(
                        choices=[],
                        label="Model",
                        interactive=True
                    )
                    
                    api_key_input = gr.Textbox(
                        label="API Key",
                        type="password",
                        placeholder="Enter your API key...",
                        lines=1
                    )
                    
                    connect_btn = gr.Button("🔌 CONNECT", variant="primary")
                
                with gr.Accordion("📊 INFO", open=False):
                    info_text = """**Commands:**
- `/help` - Show help
- `/status` - System status
- `/models` - List models
- `/new` - New session

**Features:**
- Streaming responses
- Code highlighting
- Markdown support
- Copy/paste friendly"""
                    gr.Markdown(info_text)
        
        # Footer
        footer_text = """---
<div style='text-align: center; color: #00ff41; font-family: monospace;'>
<b>HacxGPT v2.0</b> | Built with love by BlackTechX | 
<a href='https://github.com/BlackTechX011/Hacx-GPT' style='color: #00d4ff;'>GitHub</a>
</div>"""
        gr.Markdown(footer_text)
        
        # Event handlers
        def update_models(provider):
            return ui_instance.get_models_for_provider(provider)
        
        def connect_handler(provider, api_key, model):
            status = ui_instance.change_provider(provider, api_key, model)
            return status
        
        def help_handler(history):
            help_msg = ui_instance._handle_command('/help')
            history.append({"role": "user", "content": "/help"})
            history.append({"role": "assistant", "content": help_msg})
            return history
        
        def new_session_handler(history):
            ui_instance.clear_history()
            return []
        
        # Wire up events
        provider_dropdown.change(
            fn=update_models,
            inputs=[provider_dropdown],
            outputs=[model_dropdown]
        )
        
        connect_btn.click(
            fn=connect_handler,
            inputs=[provider_dropdown, api_key_input, model_dropdown],
            outputs=[status_display]
        )
        
        msg_input.submit(
            fn=ui_instance.chat,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input]
        )
        
        submit_btn.click(
            fn=ui_instance.chat,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input]
        )
        
        clear_btn.click(
            fn=lambda: [],
            outputs=[chatbot]
        )
        
        new_session_btn.click(
            fn=new_session_handler,
            inputs=[chatbot],
            outputs=[chatbot]
        )
        
        help_btn.click(
            fn=help_handler,
            inputs=[chatbot],
            outputs=[chatbot]
        )
        
        # Initialize models on load
        interface.load(
            fn=update_models,
            inputs=[provider_dropdown],
            outputs=[model_dropdown]
        )
    
    return interface, custom_css


def launch_web_ui(share=False, server_port=7860, server_name="127.0.0.1"):
    """Launch the Gradio web interface"""
    Config.initialize()
    interface, custom_css = create_ui()
    
    print("\n" + "="*60)
    print("🔥 HACXGPT NEURAL INTERFACE - WEB EDITION")
    print("="*60)
    print(f"🌐 Server starting on http://{server_name}:{server_port}")
    print("⚡ SYSTEM: UNRESTRICTED | PROTOCOL: ACTIVE")
    print("="*60 + "\n")
    
    interface.launch(
        share=share,
        server_port=server_port,
        server_name=server_name,
        show_error=True,
        quiet=False,
        css=custom_css
    )


if __name__ == "__main__":
    launch_web_ui()
