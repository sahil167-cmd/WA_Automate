import time
import random
from typing import Dict
from .logger import logger
from .config import Config

class RateLimiter:
    def __init__(self, config: Config = None):
        if config is None:
            try:
                config = Config()
            except Exception:
                config = None
        
        self.min_delay = config.get("delays", "min_delay", default=15) if config else 15
        self.max_delay = config.get("delays", "max_delay", default=45) if config else 45
        
        # Batch cooldown settings
        self.batch_size = config.get("delays", "batch_size", default=10) if config else 10
        self.batch_cooldown = config.get("delays", "batch_cooldown", default=300) if config else 300
        
        self.sent_count = 0
        self.total_wait_time = 0.0
        self.total_cooldown_time = 0.0
        self.start_time = time.time()

    def wait_between_messages(self) -> float:
        """
        Sleeps for a random duration between min_delay and max_delay.
        Returns the delay duration.
        """
        delay = random.uniform(self.min_delay, self.max_delay)
        logger.info(f"⏳ Waiting for {delay:.2f} seconds to mimic human behavior (anti-ban)...")
        time.sleep(delay)
        self.total_wait_time += delay
        
        self.sent_count += 1
        
        # Check if we reached batch limit and need a longer cooldown
        if self.sent_count % self.batch_size == 0:
            logger.info(f"⚠️ Sent {self.sent_count} messages. Triggering batch cooldown of {self.batch_cooldown} seconds...")
            
            cooldown_start = time.time()
            # Countdown timer logs
            for remaining in range(self.batch_cooldown, 0, -60):
                if remaining >= 60:
                    logger.info(f"⏳ Cooldown remaining: {remaining // 60} minute(s)...")
                    time.sleep(min(60, remaining))
                else:
                    time.sleep(remaining)
            cooldown_duration = time.time() - cooldown_start
            self.total_cooldown_time += cooldown_duration
            logger.info("✅ Cooldown complete. Resuming campaign.")
            
        return delay

    def get_metrics(self) -> Dict[str, float]:
        """
        Returns execution statistics.
        """
        elapsed = time.time() - self.start_time
        return {
            "elapsed_seconds": elapsed,
            "total_wait_seconds": self.total_wait_time,
            "total_cooldown_seconds": self.total_cooldown_time,
            "messages_processed": float(self.sent_count)
        }
