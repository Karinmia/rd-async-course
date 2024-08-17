import enum
import random

import asyncio
from asyncio import Condition


class ForkState(enum.Enum):
    FREE = 1
    TAKEN = 2


class Fork:
    
    def __init__(self, _id):
        self._id = _id
        self.state: ForkState = ForkState.FREE  # default state
        self.condition = Condition()
        
    def is_free(self):
        return self.state is ForkState.FREE
    
    def is_taken(self):
        return self.state is ForkState.TAKEN
    
    async def change_state(self, new_state: ForkState):
        async with self.condition:
            self.state = new_state
            if new_state == ForkState.FREE:
                print(f"\tFork {self._id} is released!")
            else:
                print(f"\tFork {self._id} has been taken!")
            
            self.condition.notify_all()


class Philosoph:
    
    def __init__(self, left_fork, right_fork, name):
        self.left_fork: Fork = left_fork
        self.right_fork: Fork = right_fork
        self.name = name
        
    async def take_fork(self, fork: Fork):
        print(f'Philosoph {self.name} has taken fork {fork._id}')
        await fork.change_state(ForkState.TAKEN)
    
    async def put_fork_down(self, fork: Fork):
        print(f'Philosoph {self.name} put down fork {fork._id}')
        await fork.change_state(ForkState.FREE)
        
    async def wait_for_a_fork_and_take_it(self, fork):
        async with fork.condition:
            # wait until fork is free
            await fork.condition.wait_for(fork.is_free)
        
        # take fork
        await self.take_fork(fork)

    async def think(self):
        print(f'\nPhilosoph {self.name} is thinking...')
        await asyncio.sleep(random.randint(2, 4))
        
        await asyncio.gather(
            self.wait_for_a_fork_and_take_it(self.left_fork),
            self.wait_for_a_fork_and_take_it(self.right_fork)
        )
        print(f'Philosoph {self.name} has taken both forks')
        
        await self.eat()
                
    async def eat(self):
        """Simulate eat process"""
        
        print(f'\nPhilosoph {self.name} is eating...')
        await asyncio.sleep(random.randint(1, 3))
        
        # finish eating: put down both forks
        await self.put_fork_down(self.left_fork)
        await self.put_fork_down(self.right_fork)
        
        await self.think()
    

async def start_dinner():
    # create forks
    fork1 = Fork(_id=1)
    fork2 = Fork(_id=2)
    fork3 = Fork(_id=3)
    fork4 = Fork(_id=4)
    fork5 = Fork(_id=5)
    
    # create philosophers
    phil1 = Philosoph(left_fork=fork1, right_fork=fork2, name=1)
    phil2 = Philosoph(left_fork=fork2, right_fork=fork3, name=2)
    phil3 = Philosoph(left_fork=fork3, right_fork=fork4, name=3)
    phil4 = Philosoph(left_fork=fork4, right_fork=fork5, name=4)
    phil5 = Philosoph(left_fork=fork5, right_fork=fork1, name=5)
    
    await asyncio.gather(
        phil1.think(),
        phil2.think(),
        phil3.think(),
        phil4.think(),
        phil5.think(),
    )

try:
    asyncio.run(start_dinner())
except KeyboardInterrupt:
    print("*** DONE ***")
