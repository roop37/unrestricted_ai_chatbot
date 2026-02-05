"""
HacxGPT Web UI - Gradio Interface
Plain text interface optimized for code display
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
        """Process chat message and return updated history"""
        if not self.brain:
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
                    # Update the last message with streaming response
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
            return """Available Commands:
/help - Show this help message
/status - Show current configuration
/models - List available models
/clear - Clear conversation history
/new - Start new conversation"""
        
        elif cmd == '/status':
            if not self.brain:
                return "⚠️ No active connection"
            return f"""System Status:
Provider: {self.current_provider.upper()}
Model: {self.current_model}
Status: ✓ Connected"""
        
        elif cmd == '/models':
            if not self.current_provider:
                return "⚠️ No provider selected"
            models = Config.get_provider_config(self.current_provider).get("models", [])
            model_list = "\n".join([f"• {m['name']} - {m['alias']}" for m in models])
            return f"Available Models for {self.current_provider.upper()}:\n{model_list}"
        
        elif cmd == '/clear':
            return "✓ Use the 'Clear' button to clear conversation history"
        
        elif cmd == '/new':
            if self.brain:
                self.brain.reset()
                return "✓ Memory wiped. New session started."
            return "⚠️ No active connection"
        
        else:
            return f"⚠️ Unknown command: {command}\nType /help for available commands"
    
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
    
    # Clean CSS for plain text display
    custom_css = """
    /* Color Variables */
    :root {
        --primary: #00ff41;
        --secondary: #00d4ff;
        --bg-main: #0a0e27;
        --bg-chat: #0d1117;
        --bg-user: #161b22;
        --bg-bot: #0d1117;
        --text: #c9d1d9;
        --text-dim: #8b949e;
        --border: #30363d;
    }
    
    /* Main */
    .gradio-container {
        background: var(--bg-main) !important;
    }
    
    /* Header */
    h1 {
        color: var(--primary) !important;
        font-size: 24px !important;
        margin: 8px 0 !important;
        text-shadow: 0 0 20px rgba(0, 255, 65, 0.4) !important;
    }
    
    h3 {
        color: var(--secondary) !important;
        font-size: 13px !important;
        margin: 0 0 16px 0 !important;
    }
    
    /* Chat Container - PLAIN TEXT */
    .chatbot {
        background: var(--bg-chat) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
    }
    
    /* Message rows */
    .message-row {
        padding: 16px 20px !important;
        border-bottom: 1px solid var(--border) !important;
    }
    
    .message-row:last-child {
        border-bottom: none !important;
    }
    
    .user .message-row {
        background: var(--bg-user) !important;
    }
    
    .bot .message-row {
        background: var(--bg-bot) !important;
    }
    
    /* Message content - PLAIN TEXT */
    .message {
        color: var(--text) !important;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
    }
    
    /* User label */
    .user-row {
        color: var(--primary) !important;
        font-weight: bold !important;
        margin-bottom: 6px !important;
    }
    
    /* Bot label */
    .bot-row {
        color: var(--secondary) !important;
        font-weight: bold !important;
        margin-bottom: 6px !important;
    }
    
    /* Input */
    textarea {
        background: var(--bg-user) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-size: 14px !important;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
        line-height: 1.5 !important;
    }
    
    textarea:focus {
        border-color: var(--primary) !important;
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(0, 255, 65, 0.2) !important;
    }
    
    /* Buttons */
    button {
        background: var(--bg-user) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 6px !important;
        padding: 10px 16px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
    }
    
    button:hover {
        background: #1c2128 !important;
        border-color: var(--primary) !important;
    }
    
    button.primary,
    .primary button {
        background: var(--primary) !important;
        color: var(--bg-main) !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    button.primary:hover,
    .primary button:hover {
        background: var(--secondary) !important;
        box-shadow: 0 0 16px rgba(0, 255, 65, 0.3) !important;
    }
    
    /* Dropdowns */
    select {
        background: var(--bg-user) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 6px !important;
        padding: 9px 12px !important;
        font-size: 14px !important;
    }
    
    /* Labels */
    label {
        color: var(--text-dim) !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Accordion */
    .accordion {
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        background: transparent !important;
    }
    
    /* Status textbox */
    .textbox-container textarea {
        background: #010409 !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        font-family: 'Consolas', monospace !important;
        font-size: 13px !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-main);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 16px;
        color: var(--text-dim);
        font-size: 12px;
        border-top: 1px solid var(--border);
        margin-top: 16px;
    }
    
    .footer a {
        color: var(--secondary);
        text-decoration: none;
    }
    """
    
    with gr.Blocks(title="HacxGPT") as interface:
        
        # Header
        gr.HTML("""
        <h1>🔥 HACXGPT</h1>
        <h3>NEURAL INTERFACE</h3>
        """)
        
        with gr.Row():
            # Main chat (75%)
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="",
                    height=600,
                    show_label=False,
                    render_markdown=False
                )
                
                with gr.Row():
                    msg_input = gr.Textbox(
                        label="",
                        placeholder="Message HacxGPT... (type /help for commands)",
                        lines=2,
                        max_lines=8,
                        show_label=False,
                        scale=9
                    )
                    submit_btn = gr.Button("⚡ SEND", scale=1, variant="primary")
                
                with gr.Row():
                    clear_btn = gr.Button("Clear", size="sm")
                    new_btn = gr.Button("New", size="sm")
                    help_btn = gr.Button("Help", size="sm")
            
            # Sidebar (25%)
            with gr.Column(scale=1, min_width=250):
                with gr.Accordion("⚙️ CONFIG", open=True):
                    status_display = gr.Textbox(
                        label="Status",
                        value="⚠️ Not Connected",
                        interactive=False,
                        lines=3
                    )
                    
                    provider_dropdown = gr.Dropdown(
                        choices=list(Config.PROVIDERS.keys()),
                        value=list(Config.PROVIDERS.keys())[0] if Config.PROVIDERS else None,
                        label="Provider"
                    )
                    
                    model_dropdown = gr.Dropdown(
                        choices=[],
                        label="Model"
                    )
                    
                    api_key_input = gr.Textbox(
                        label="API Key",
                        type="password",
                        placeholder="sk-...",
                        lines=1
                    )
                    
                    connect_btn = gr.Button("🔌 Connect", variant="primary")
                
                with gr.Accordion("ℹ️ INFO", open=False):
                    gr.HTML("""
                    <div style="color: #8b949e; font-size: 13px; line-height: 1.6;">
                    <strong>Commands:</strong><br>
                    • /help - Show help<br>
                    • /status - System info<br>
                    • /new - New session<br><br>
                    <strong>Tips:</strong><br>
                    • Plain text mode<br>
                    • Shift+Enter = newline<br>
                    • Select to copy
                    </div>
                    """)
        
        # Footer
        gr.HTML('<div class="footer">HacxGPT v2.0 | <a href="https://github.com/BlackTechX011/Hacx-GPT">GitHub</a></div>')
        
        # Event Handlers
        def update_models(provider):
            return ui_instance.get_models_for_provider(provider)
        
        def connect_handler(provider, api_key, model):
            return ui_instance.change_provider(provider, api_key, model)
        
        def help_handler(history):
            msg = ui_instance._handle_command('/help')
            history.append(["You", "/help"])
            history.append(["HacxGPT", msg])
            return history
        
        def new_handler(history):
            ui_instance.clear_history()
            return []
        
        # Wire Events
        provider_dropdown.change(update_models, [provider_dropdown], [model_dropdown])
        connect_btn.click(connect_handler, [provider_dropdown, api_key_input, model_dropdown], [status_display])
        
        msg_input.submit(ui_instance.chat, [msg_input, chatbot], [chatbot, msg_input])
        submit_btn.click(ui_instance.chat, [msg_input, chatbot], [chatbot, msg_input])
        
        clear_btn.click(lambda: [], None, [chatbot])
        new_btn.click(new_handler, [chatbot], [chatbot])
        help_btn.click(help_handler, [chatbot], [chatbot])
        
        # Initialize
        interface.load(update_models, [provider_dropdown], [model_dropdown])
    
    return interface, custom_css


def find_available_port(start_port=7860, max_port=9000):
    """Find an available port"""
    import socket
    for port in range(start_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return start_port


def launch_web_ui(share=False, server_port=7860, server_name="127.0.0.1"):
    """Launch the web interface"""
    Config.initialize()
    interface, custom_css = create_ui()
    
    if server_port == 7860:
        port = find_available_port(7860, 9000)
        if port != 7860:
            print(f"\n⚠️  Port 7860 in use, using {port}")
        server_port = port
    
    print("\n" + "="*50)
    print("🔥 HACXGPT NEURAL INTERFACE")
    print("="*50)
    print(f"🌐 http://{server_name}:{server_port}")
    print("="*50 + "\n")
    
    try:
        interface.launch(
            share=share,
            server_port=server_port,
            server_name=server_name,
            show_error=True,
            quiet=False,
            css=custom_css
        )
    except OSError as e:
        if "port" in str(e).lower():
            new_port = find_available_port(server_port + 1, 9000)
            if new_port > server_port:
                print(f"✓ Using port {new_port}\n")
                interface.launch(share=share, server_port=new_port, server_name=server_name, show_error=True, quiet=False, css=custom_css)
            else:
                raise
        else:
            raise


if __name__ == "__main__":
    launch_web_ui()