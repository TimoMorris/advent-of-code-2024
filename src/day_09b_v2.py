from day_09 import get_day_09_input

class MemoryUnit:
    """A contiguous piece of memory in the filesystem.

    `start` is the index of the first block this memory unit occupies in the filesystem
    and `end` is the index *after* the final block it occupies,
    such that `range(start, end)` returns the indices of all the blocks it occupies.
    They are both initially None; they are assigned by the filesystem when inserting the unit.

    """
    def __init__(self, size: int):
        self.size: int = size
        self.start: int | None = None
        self.end: int | None = None


class File(MemoryUnit):
    """A file in the filesystem."""
    def __init__(self, size: int, file_id: int):
        super().__init__(size)
        self.file_id = file_id


class Space(MemoryUnit):
    """A contiguous piece of empty space in the filesystem."""
    def __init__(self, size: int):
        super().__init__(size)


class FileSystem:
    """A filesystem comprising blocks of memory with files and spaces.

    `memory` is a list with each list element representing a block in the filesystem.
    Each element references the 'memory unit' (file or space) that occupies that block,
    such that a file or space of size `n` will be referenced by `n` sequential list elements.

    Each memory unit keeps track of the start and end blocks it occupies,
    making it easy to directly fetch the previous or next unit.

    """
    def __init__(self, disk_map: str):
        self.files: list[File] = []
        self.total_size: int = 0
        self.memory: list[MemoryUnit | None] = []

        memory_units, self.files, self.total_size = self.create_memory_units(disk_map)
        self.fill_memory(memory_units)

    @staticmethod
    def create_memory_units(disk_map: str) -> tuple[list[MemoryUnit], list[File], int]:
        """Create the files and empty spaces defined by the disk map.

        Only creates the right size and type; assigning start and end is done when inserting into the filesystem.

        """
        memory_units = []
        files = []  # keep a separate reference to all files for easy iterating later
        total_size = 0

        memory_type = True  # True is a file, False is a space
        file_id = 0
        for x in disk_map:
            size = int(x)
            total_size += size
            if size == 0:  # skip blocks of 0 width
                memory_type = not memory_type
                continue
            if memory_type:
                unit = File(size, file_id)
                files.append(unit)
                file_id += 1
            else:
                unit = Space(size)
            memory_units.append(unit)
            memory_type = not memory_type

        return memory_units, files, total_size

    def fill_memory(self, memory_units: list[MemoryUnit]) -> None:
        """Put memory units into filesystem memory."""
        self.memory: list[MemoryUnit | None] = [None] * (self.total_size + 1)  # extra space for tail/head unit
        current_pos: int = 0

        for unit in memory_units:
            self.insert_unit(unit, current_pos)
            current_pos += unit.size
        assert current_pos == self.total_size  # check we've filled anticipated space

        # add dummy unit at end to cope with overflow when getting next on final unit
        # or underflow when getting previous on first unit (will index into -1, which is just the final list element)
        dummy = MemoryUnit(0)
        self.memory[self.total_size] = dummy
        assert self.memory[-1] is dummy

        assert all(m is not None for m in self.memory)  # check all memory blocks filled

    def insert_unit(self, unit: MemoryUnit, position: int) -> None:
        """Insert a memory unit at the given position."""
        if position >= self.total_size:
            raise ValueError(f"Position {position} is out of range")
        
        unit.start = position
        unit.end = position + unit.size
        for i in range(unit.start, unit.end):  # give each block it occupies a reference to the memory unit
            self.memory[i] = unit
    
    def insert_file(self, file: File, position: int) -> None:
        """Insert a file at the given position, maintaining any leftover space."""
        if position >= self.total_size:
            raise ValueError(f"Position {position} is out of range")
        
        target_unit = self.memory[position]
        if not isinstance(target_unit, Space):
            raise ValueError("Can only insert files into space")

        space_size = target_unit.size
        file_size = file.size
        if space_size < file_size:
            raise ValueError("Space is not big enough for file")

        self.insert_unit(file, position)
        if space_size > file_size:  # if the file didn't fill the space, add back a unit with the remaining space
            self.insert_unit(Space(space_size - file_size), position + file_size)
    
    def remove_file(self, file: File) -> File:
        """Remove a file and return it, collating the resulting space."""
        new_space_start = file.start
        new_space_end = file.end

        previous_unit = self.memory[file.start - 1]
        next_unit = self.memory[file.end]
        if isinstance(previous_unit, Space):  # check for merging with previous space
            new_space_start = previous_unit.start
        if isinstance(next_unit, Space):  # check for merging with next space
            new_space_end = next_unit.end

        new_space_size = new_space_end - new_space_start
        new_space = Space(new_space_size)
        self.insert_unit(new_space, new_space_start)

        # remove file index references for safety
        file.start = None
        file.end = None
        return file

    def traverse(self):
        """Iterate over the memory units in the filesystem."""
        current_pos = 0
        while current_pos < self.total_size:
            yield self.memory[current_pos]
            current_pos = self.memory[current_pos].end

    def find_space(self, min_size: int, before_unit: MemoryUnit) -> Space | None:
        """Search from left to right, up to the given memory unit, for a space of at least the given size."""
        for unit in self.traverse():
            if unit is before_unit:  # not found a space of the right size before the limit point
                return
            if isinstance(unit, Space) and unit.size >= min_size:
                return unit

    def get_checksum(self):
        """Calculate the checksum for the filesystem."""
        checksum = 0

        for unit in self.traverse():
            if isinstance(unit, File):
                checksum += sum(range(unit.start, unit.end)) * unit.file_id

        return checksum


def day_09b_v2(disk_map: str) -> int:
    file_system = FileSystem(disk_map)

    for file in reversed(file_system.files):
        if (space := file_system.find_space(file.size, file)) is not None:
            file_system.remove_file(file)
            file_system.insert_file(file, space.start)

    checksum = file_system.get_checksum()
    return checksum


if __name__ == "__main__":
    day_09_input = get_day_09_input()
    answer_09b = day_09b_v2(day_09_input)
    print(answer_09b)
