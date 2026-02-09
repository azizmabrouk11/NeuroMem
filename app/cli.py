"""
Command-line interface for the AI Brain memory system.
Provides interactive testing of memory operations.
"""

import sys
from typing import Optional
import click
from loguru import logger
from datetime import datetime

from core.brain import Brain
from models.memory import MemoryType


logger.remove()
logger.add(sys.stderr, level="INFO")

@click.group()
def cli():
    """AI Brain Memory System CLI"""
    pass


@cli.command()
@click.argument('content')
@click.option('--user-id', '-u', default='default_user', help='User ID')
@click.option('--type', '-t', 
              type=click.Choice(['episodic', 'semantic'], case_sensitive=False),
              default='episodic',
              help='Memory type')
@click.option('--importance', '-i', type=float, default=None, help='Importance score (0.0-1.0)')
@click.option('--tags', '-g', multiple=True, help='Tags (can specify multiple)')
def remember(content: str, user_id: str, type: str, importance: Optional[float], tags: tuple):
    """
    Store a new memory.
    
    Example:
        python -m app.cli remember "I love spicy food" -u aziz -t semantic -g food -g preference
    """
    try:
        brain = Brain(user_id=user_id)
        
        memory_type = MemoryType.SEMANTIC if type == 'semantic' else MemoryType.EPISODIC
        
        memory = brain.remember(
            content=content,
            memory_type=memory_type,
            importance_score=importance,
            tags=list(tags) if tags else None
        )
        
        click.echo(click.style("✓ Memory stored successfully!", fg='green', bold=True))
        click.echo(f"  ID: {memory.id}")
        click.echo(f"  Content: {memory.content}")
        click.echo(f"  Type: {memory.memory_type.value}")
        click.echo(f"  Importance: {memory.importance_score:.2f}")
        click.echo(f"  Tags: {', '.join(memory.tags) if memory.tags else 'None'}")
        
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red', bold=True))
        sys.exit(1)


@cli.command()
@click.argument('query')
@click.option('--user-id', '-u', default='default_user', help='User ID')
@click.option('--type', '-t', 
              type=click.Choice(['episodic', 'semantic'], case_sensitive=False),
              multiple=True,
              help='Filter by memory type')
@click.option('--top-k', '-k', default=5, help='Number of results')
@click.option('--min-similarity', '-s', default=0.5, help='Minimum similarity (0.0-1.0)')
@click.option('--tags', '-g', multiple=True, help='Filter by tags')
def recall(query: str, user_id: str, type: tuple, top_k: int, min_similarity: float, tags: tuple):
    """
    Search for relevant memories.
    
    Example:
        python -m app.cli recall "what food do I like?" -u aziz -k 3
    """
    try:
        brain = Brain(user_id=user_id)
        
        # Convert type strings to MemoryType enums
        memory_types = None
        if type:
            memory_types = [
                MemoryType.SEMANTIC if t == 'semantic' else MemoryType.EPISODIC 
                for t in type
            ]
        
        results = brain.recall(
            query=query,
            memory_types=memory_types,
            top_k=top_k,
            min_similarity=min_similarity,
            tags=list(tags) if tags else None
        )
        
        if not results:
            click.echo(click.style("No memories found.", fg='yellow'))
            return
        
        click.echo(click.style(f"\n✓ Found {len(results)} memories:", fg='green', bold=True))
        click.echo()
        
        for i, result in enumerate(results, 1):
            memory = result.memory
            
            click.echo(click.style(f"[{i}] ", fg='cyan', bold=True) + 
                      click.style(memory.content, bold=True))
            click.echo(f"    ID: {memory.id}")
            click.echo(f"    Type: {memory.memory_type.value}")
            click.echo(f"    Similarity: {result.similarity_score:.3f}")
            click.echo(f"    Final Score: {result.final_score:.3f}")
            click.echo(f"    Importance: {memory.importance_score:.2f}")
            click.echo(f"    Created: {memory.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            click.echo(f"    Access Count: {memory.access_count}")
            if memory.tags:
                click.echo(f"    Tags: {', '.join(memory.tags)}")
            click.echo()
        
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red', bold=True))
        sys.exit(1)


@cli.command()
@click.argument('memory_id')
@click.option('--user-id', '-u', default='default_user', help='User ID')
def forget(memory_id: str, user_id: str):
    """
    Delete a memory by ID.
    
    Example:
        python -m app.cli forget mem_abc123 -u aziz
    """
    try:
        brain = Brain(user_id=user_id)
        
        success = brain.forget(memory_id)
        
        if success:
            click.echo(click.style(f"✓ Memory {memory_id} deleted successfully!", fg='green', bold=True))
        else:
            click.echo(click.style(f"✗ Failed to delete memory {memory_id}", fg='red', bold=True))
            sys.exit(1)
        
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red', bold=True))
        sys.exit(1)


@cli.command()
@click.argument('query')
@click.option('--user-id', '-u', default='default_user', help='User ID')
@click.option('--max-memories', '-m', default=10, help='Max memories to include')
def context(query: str, user_id: str, max_memories: int):
    """
    Get formatted context for LLM.
    
    Example:
        python -m app.cli context "What are my preferences?" -u aziz
    """
    try:
        brain = Brain(user_id=user_id)
        
        context_str = brain.get_context(query, max_memories=max_memories)
        
        click.echo(click.style("\n=== LLM Context ===", fg='cyan', bold=True))
        click.echo(context_str)
        click.echo(click.style("==================\n", fg='cyan', bold=True))
        
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red', bold=True))
        sys.exit(1)


@cli.command()
@click.option('--user-id', '-u', default='default_user', help='User ID')
def stats(user_id: str):
    """
    Show memory statistics for a user.
    
    Example:
        python -m app.cli stats -u aziz
    """
    try:
        # This is a simple implementation
        # You could add a proper stats method to Brain later
        click.echo(click.style(f"\n📊 Memory Statistics for user: {user_id}", fg='cyan', bold=True))
        click.echo()
        click.echo("Note: Detailed stats coming soon!")
        click.echo("Use 'recall' with broad queries to see your memories.")
        
    except Exception as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red', bold=True))
        sys.exit(1)


if __name__ == '__main__':
    cli()