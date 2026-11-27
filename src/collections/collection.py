from typing import Any, Iterator, TypeVar, Generic, Self

# restrict generic type T to only accept given types
#T = TypeVar('T', str, int, 'Collection[int]', 'Collection[str]')
T = TypeVar('T')
class Collection(Generic[T]):
    """
    Generic collection class of type T with basic collection operations.
    See: https://sgra64.github.io/py-fun.github.io/src.collections.html.
    """

    def __init__(self, *args, asSet=False):
        """
        Constructor of a Collection.

        Args:
            args: elements added to the Collection including
            number or string literals, sets and lists.
        """
        self._items = set() if asSet else list()
        for arg in args:
            self.add(arg)

    def add(self, item: T) -> Self:
        """
        Add an element of type T to the collection.

        Args:
            item: element to add to the collection.

        Returns:
            Chainable self-reference to the collection with the element added.
        """
        item = item if not isinstance(item, set | dict) else frozenset(item) # type: ignore
        if isinstance(self._items, list):
            self._items.append(item)
        else:
            # list cannot be added to a set since lists are mutable and therefore unhashable.
            self._items.add(item if not isinstance(item, list) else tuple(item))
        return self

    def contains(self, item: Any) -> bool:
        """
        Test that an item or subset exists in the collection.

        Args:
            item: element to test that it is in the collection.

        Returns:
            True if element is in the collection, False otherwise.
        """
        return item in self._items

    def size(self) -> int:
        """
        Returns the number of items in the collection.

        Returns:
            the number of items in the collection.
        """
        return len(self._items)

    @classmethod
    def zip(cls, l1: 'Collection', l2: 'Collection') -> 'Collection[tuple]':
        """
        Return a new collection of two-item tuples zipped from the input collections.
        """
        result: Collection[tuple] = Collection()
        for pair in zip(l1, l2):
            result.add(pair) # type: ignore
        return result # type: ignore

    def pset(_self) -> set[frozenset[T]]:
        """
        Return the power set of this Collection using backtracking.

        Returns:
            The power set of this Collection.
        """
        return {frozenset(subset) for subset in _self.pset_gen()}

    def pset_gen(self) -> Iterator['set[T]']:
        """
        Generator that yields each subset using backtracking.
        
        Returns:
            Generator object for the power set of this Collection.
        """
        items = list(self._items)
        current = set()

        def backtrack(index):
            if index == len(items):
                yield current.copy()
                return

            yield from backtrack(index + 1)

            current.add(items[index])
            yield from backtrack(index + 1)
            current.remove(items[index])

        yield from backtrack(0)

    def perm(self) -> list[list[T]]:
        """
        Return all permutations of this Collection.

        Returns:
            The list of permutations of this Collection.
        """
        return list(self.perm_gen())

    def perm_gen(self) -> Iterator[list[T]]:
        """"
        Generator that yields permutations using backtracking.

        Returns:
            Generator object for the list of permutations of this Collection.
        """
        items = list(self._items)
        used = [False] * len(items)
        current = []

        def backtrack():
            if len(current) == len(items):
                yield current.copy()
                return

            for i in range(len(items)):
                if not used[i]:
                    used[i] = True
                    current.append(items[i])

                    yield from backtrack()

                    current.pop()
                    used[i] = False

        yield from backtrack()


    def __contains__(self, item: Any) -> bool:
        """Checks if an item or subset exists in the collection (in-operator)."""
        return item in self._items

    def __len__(self) -> int:
        """Returns the number of items in the collection, invoked by len()."""
        return len(self._items)

    def __iter__(self) -> Iterator[Any]:
        """Returns an iterator over the items in the collection, invoked in loops."""
        return iter(self._items)

    def __repr__(self):
        """Custom representation for str() that formats inner frozenSets as { }."""
        elements = []
        for item in self._items:
            if isinstance(item, set | frozenset):
                elements.append(f"{{{", ".join(repr(e) for e in item)}}}")
            else:
                elements.append(repr(item))
        # 
        r = f"{', '.join(elements)}"
        return f"[{r}]" if isinstance(self._items, list) else f"{{{r}}}"
