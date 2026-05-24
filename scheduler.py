import time
import random
from logger import logger
from config import Config

class RateLimiter:
    def __init__(self, config: Config = None):
        if config is None:
            config = Config()
        
        self.min_delay = config.get("delays", "min_delay", default=15)
        self.max_delay = config.get("delays", "max_delay", default=45)
        
        # Batch cooldown settings
        self.batch_size = config.get("delays", "batch_size", default=10)
        self.batch_cooldown = config.get("delays", "batch_cooldown", default=300) # 5 minutes default
        
        self.sent_count = 0

    def wait_between_messages(self):
        """Sleeps for a random duration between min_delay and max_delay."""
        delay = random.uniform(self.min_delay, self.max_delay)
        logger.info(f"⏳ Waiting for {delay:.2f} seconds to mimic human behavior (anti-ban)...")
        time.sleep(delay)
        
        self.sent_count += 1
        
        # Check if we reached batch limit and need a longer cooldown
        if self.sent_count % self.batch_size == 0:
            logger.info(f"⚠️ Sent {self.sent_count} messages. Triggering batch cooldown of {self.batch_cooldown} seconds...")
            # Countdown timer logs
            for remaining in range(self.batch_cooldown, 0, -60):
                if remaining >= 60:
                    logger.info(f"⏳ Cooldown remaining: {remaining // 60} minute(s)...")
                    time.sleep(min(60, remaining))
                else:
                    time.sleep(remaining)
            logger.info("✅ Cooldown complete. Resuming campaign.")
