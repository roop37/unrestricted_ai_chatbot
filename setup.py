from setuptools import setup, find_packages

setup(
    name="hacxgpt",
    version="2.0.0",
    description="Advanced Uncensored AI Terminal Interface",
    author="BlackTechX",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "hacxgpt": ["providers.json", "prompts/*.md"],
    },
    install_requires=[
        "openai",
        "rich",
        "python-dotenv",
        "pwinput",
        "pyperclip",
        "colorama",
        "prompt_toolkit",
        "gradio>=4.0.0"
    ],
    entry_points={
        "console_scripts": [
            "hacxgpt=hacxgpt.main:main",
            "hacxgpt-web=hacxgpt.web_ui:launch_web_ui",
        ],
    },
    python_requires=">=3.8",
)

