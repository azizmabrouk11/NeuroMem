"""
Temporal decay functions for memory relevance.
Recent memories have higher weight, old memories decay over time.

"""

from datetime import datetime, timezone
import math
from models.memory import Memory
from config.settings import settings


class TemporalDecay:
    
    def __init__(self, decay_rate: float = 0.1):
        """
        Applies time-based decay to memory scores.
        
        Formula: decay_factor = exp(-decay_rate * days_elapsed)
        
        Example:
            - Memory from today: decay_factor ≈ 1.0
            - Memory from 30 days ago: decay_factor ≈ 0.74 (with default decay_rate=0.01)
            - Memory from 90 days ago: decay_factor ≈ 0.41
        """
        self.decay_rate = decay_rate or settings.decay_rate

    def calculate_decay(self,memory : Memory)->float:
        """
        Calculate decay factor for a memory based on age.
        
        Args:
            memory: Memory object with timestamp
            
        Returns:
            Decay factor between 0.0 and 1.0
        """
    
        now = datetime.now(timezone.utc)
        
        memory_time = memory.timestamp
        if memory_time.tzinfo is None:
            memory_time = memory_time.replace(tzinfo=timezone.utc)

        
        time_elapsed = (now - memory_time).total_seconds() 
        days_elapsed = time_elapsed / 86400
        decay_factor = math.exp(-self.decay_rate * days_elapsed)

        return decay_factor 
    

    