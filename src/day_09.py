from collections import deque


def get_day_09_input() -> str:
    with open("inputs/input_09.txt") as f:
        contents = f.read()

    return contents


def create_disk_layout(disk_map: str) -> list[bool]:
    """Create a disk layout list from a disk map.

    Take the disk map dense format string and return a list of boolean values representing the disk layout,
    where True indicates a file and False a free space.

    """
    disk_layout = []
    block_type = True
    for x in disk_map:
        disk_layout.extend([block_type] * int(x))
        block_type = not block_type
    return disk_layout


def create_file_blocks(disk_map: str) -> list[int]:
    """Create a file blocks list from a disk map.

    Take the disk map dense format string and return a sequential list of file IDs,
    with each ID repeated to match its block size.

    """
    file_blocks = []
    file_id = 0
    for x in disk_map[::2]:
        file_blocks.extend([file_id] * int(x))
        file_id += 1
    return file_blocks


def move_blocks(disk_layout: list[bool], file_blocks: list[int]) -> list[int]:
    """Create final disk layout with moved blocks."""
    file_deque = deque(file_blocks)

    final_layout = []
    for block in disk_layout:
        if block:
            final_layout.append(file_deque.popleft())
        else:
            final_layout.append(file_deque.pop())
        if not file_deque:  # check whether there are files left to move
            break

    return final_layout


def calculate_filesystem_checksum(layout: list[int]):
    """Calculate the filesystem checksum for the given file layout."""
    checksum = sum(pos * file_id for pos, file_id in enumerate(layout))
    return checksum


def day_09a(disk_map: str) -> int:
    disk_layout = create_disk_layout(disk_map)
    file_blocks = create_file_blocks(disk_map)

    final_layout = move_blocks(disk_layout, file_blocks)
    checksum = calculate_filesystem_checksum(final_layout)
    return checksum


class Block:
    """A contiguous piece of memory in the filesystem."""
    def __init__(self, size: int, prev=None, next_=None):
        self.size = size
        self.prev = prev
        self.next = next_

    def insert_after(self, block: "Block"):
        """Insert the block before this one."""
        original_next = self.next
        original_next.prev = block
        block.next = original_next
        block.prev = self
        self.next = block

    def insert_before(self, block: "Block"):
        """Insert the block after this one."""
        original_prev = self.prev
        original_prev.next = block
        block.prev = original_prev
        block.next = self
        self.prev = block


class FileBlock(Block):
    """A file on the filesystem."""
    def __init__(self, size: int, file_id: int):
        super().__init__(size)
        self.file_id = file_id

    def remove(self):
        """Remove this file from the filesystem, leaving empty space."""
        new_size = self.size
        new_prev = self.prev
        new_next = self.next

        original_prev = self.prev
        original_next = self.next
        if isinstance(original_prev, EmptyBlock):
            new_prev = original_prev.prev
            new_size += original_prev.size
        if isinstance(original_next, EmptyBlock):
            new_next = original_next.next
            new_size += original_next.size

        new_empty_block = EmptyBlock(new_size, new_prev, new_next)
        new_prev.next = new_empty_block
        new_next.prev = new_empty_block

        return self


class EmptyBlock(Block):
    """A contiguous piece of empty space on the filesystem."""
    def __init__(self, size: int, prev=None, next_=None):
        super().__init__(size, prev, next_)

    def insert_file(self, file: FileBlock):
        """Insert a file into this empty space."""
        if file.size > self.size:
            raise ValueError("Space is not big enough for file")

        self.insert_before(file)
        self.size -= file.size
        if self.size == 0:
            self.remove()

    def remove(self):
        """Remove this empty space (only valid if the space has no size)."""
        if self.size != 0:
            raise ValueError("Cannot remove non-zero space")

        original_prev = self.prev
        original_next = self.next
        original_prev.next = original_next
        original_next.prev = original_prev

        return self


class FileSystem:
    """"""
    def __init__(self, disk_map: str):
        all_blocks, file_blocks = self.create_blocks(disk_map)
        self.head, self.tail = self.link_blocks(all_blocks)
        self.file_blocks = file_blocks

    @staticmethod
    def create_blocks(disk_map: str) -> tuple[list[Block], list[FileBlock]]:
        all_blocks = []
        file_blocks = []

        block_type = True
        file_id = 0
        for x in disk_map:
            size = int(x)
            if size == 0:  # skip blocks of 0 width
                block_type = not block_type
                continue
            if block_type:
                block = FileBlock(size, file_id)
                file_blocks.append(block)
                file_id += 1
            else:
                block = EmptyBlock(size)
            all_blocks.append(block)
            block_type = not block_type

        return all_blocks, file_blocks

    @staticmethod
    def link_blocks(blocks: list[Block]):
        head = Block(0)
        tail = Block(0)

        prev = head
        for block in blocks + [tail]:
            prev.next = block
            block.prev = prev
            prev = block

        return head, tail

    def traverse(self):
        current = self.head
        while current is not self.tail:
            current = current.next
            yield current

    def find_empty_block(self, min_size: int, before_block: Block) -> EmptyBlock | None:
        for block in self.traverse():
            if block is before_block:  # not found an empty block of the right size before the limit point
                return
            if isinstance(block, EmptyBlock) and block.size >= min_size:
                return block

    def get_checksum(self):
        checksum = 0

        pos = 0
        for block in self.traverse():
            if isinstance(block, FileBlock):
                checksum += sum(range(pos, pos + block.size)) * block.file_id
            pos += block.size

        return checksum


def day_09b(disk_map: str) -> int:
    file_system = FileSystem(disk_map)

    for file in reversed(file_system.file_blocks):
        if (space := file_system.find_empty_block(file.size, file)) is not None:
            file.remove()
            # .prev.next to deal with edge-case when we've removed `space` due to merging (and replacing with new instance)
            # occurs when we're moving file into an adjacent space
            space.prev.next.insert_file(file)

    checksum = file_system.get_checksum()
    return checksum


if __name__ == "__main__":
    day_09_input = get_day_09_input()
    answer_09a = day_09a(day_09_input)
    print(answer_09a)
    answer_09b = day_09b(day_09_input)
    print(answer_09b)
