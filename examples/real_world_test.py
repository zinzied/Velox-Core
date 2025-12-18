import asyncio
import sys
import os
from rich.console import Console

# Add current directory to path so we can import velox
sys.path.append(os.getcwd())

from velox.core.engine import Velox
from velox.providers.google import GoogleGeminiProvider
from velox.layers.advanced_dashboard import AdvancedDashboardLayer
from velox.layers.pii_guard import PIIGuardLayer

console = Console()

async def main():
    # Load Gemini API Key from environment
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        console.print("[bold yellow]No GOOGLE_API_KEY found in environment.[/bold yellow]")
        api_key = console.input("Please enter your Gemini API key: ")
    
    if not api_key:
        console.print("[bold red]No API key provided. Exiting.[/bold red]")
        return
    
    motor = Velox()
    
    # 1. Enable Advanced Dashboard for visual feedback
    motor.add(AdvancedDashboardLayer())
    
    # 2. Add PII Guard to test security middleware
    motor.add(PIIGuardLayer())
    
    # 3. Use Google Gemini Provider
    try:
        motor.use(GoogleGeminiProvider(api_key=api_key, model="gemini-flash-latest"))
        console.print("[green]✅ Provider initialized.[/green]")
    except Exception as e:
        console.print(f"[red]❌ Error initializing provider:[/red] {e}")
        return

    # 4. Run a test prompt with some PII to test the guard
    test_prompt = "Hello! My name is John Doe, my email is john.doe@example.com and my phone number is +1-555-0199. Can you summarize the importance of Velox in one sentence?"
    
    console.print(f"\n[bold]Sending Prompt:[/bold]\n{test_prompt}\n")
    
    try:
        response = await motor.prompt(test_prompt)
        console.print(f"\n[bold green]Velox Response:[/bold green]\n{response}")
    except Exception as e:
        console.print(f"\n[bold red]Error during prompt:[/bold red] {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Test interrupted by user.[/yellow]")
    except Exception as e:
        console.print(f"[bold red]Fatal error:[/bold red] {e}")
