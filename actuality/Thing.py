class Universe:
	def __init__(self, name):
		self._name = str(name)
		self._ids_to_things = {}
		self._names_to_ids = {}
		self._next_id = 0
		self._available_ids = set()

		self._left_to_relationships = {}
		self._middle_to_relationships = {}
		self._right_to_relationships = {}

	@property
	def name(self):
		"""
		:rtype: str
		"""
		return self._name

	def get_new_id(self):
		if len(self._available_ids) > 0:
			return self._available_ids.pop()
		else:
			return self._next_id

	def add_thing(self, name, value=None):
		"""
		add a thing to the universe
		:type name: str
		:rtype:
		"""
		return Thing(universe=self, name=name, value=value)

	def add_relationship(self, thing1, thing2, thing3):
		"""
		:type thing1:
		:type thing2:
		:type thing3:
		:rtype: Relationship
		"""
		thing1 = self.get_thing(key=thing1)
		thing2 = self.get_thing(key=thing2)
		thing3 = self.get_thing(key=thing3)

		return Relationship(thing1=thing1, thing2=thing2, thing3=thing3)

	def get_thing(self, key):
		"""
		returns a thing with a name or id
		:type key: str or int or Thing
		:rtype: Thing
		"""
		if isinstance(key, Thing):
			key = key.id

		if isinstance(key, str):
			id = self._names_to_ids[key]
			return self._ids_to_things[id]
		elif isinstance(key, int):
			return self._ids_to_things[key]
		else:
			raise TypeError(f'Type {type(key)} is not supported!')

	def contains(self, item):
		if isinstance(item, Thing):
			if item.id in self._ids_to_things and item.name in self._names_to_ids:
				return True
			elif item.id not in self._ids_to_things and item.name not in self._names_to_ids:
				return False
			elif item.id in self._ids_to_things and item.name not in self._names_to_ids:
				raise RuntimeError('This is impossible! The id exists but the name does not!')
			else:
				raise RuntimeError('This is impossible! The name exists but the id does not!')

		elif isinstance(item, int):
			if item in self._ids_to_things:
				thing = self._ids_to_things[item]
				if thing.name in self._names_to_ids:
					return True
				else:
					raise RuntimeError('This is impossible! The id exists but the name does not!')
			else:
				return False

		elif isinstance(item, str):
			if item in self._names_to_ids:
				_id = self._names_to_ids[item]
				if _id in self._ids_to_things:
					return True
				else:
					raise RuntimeError('This is impossible! The name exists but the id does not!')
			else:
				return False
		else:
			raise TypeError(f'Type {type(item)} is not supported!')



	def remove_thing(self, name_or_id):
		if isinstance(name_or_id, Thing):
			thing = name_or_id
		else:
			thing = self.get_thing(key=name_or_id)

		self._available_ids.add(thing.id)
		del self._ids_to_things[thing.id]
		del self._names_to_ids[thing.name]

	def remove_relationship(self, name_or_id):

	def __getitem__(self, item):
		return self.get_thing(key=item)

	def __delitem__(self, key):
		return self.remove_thing(name_or_id=key)

	def __del__(self):
		for _id, thing in self._ids_to_things.items():
			self.remove_thing(name_or_id=_id)

	def __contains__(self, item):
		return self.contains(item=item)


class Thing:
	def __init__(self, universe, name, value=None):
		"""
		creates a new thing
		:type universe: Universe
		:type name: str
		"""
		self._universe = universe
		self._name = str(name)
		self._value = value
		self._id = universe.get_new_id()
		self._left_of_relationships = {}
		self._middle_of_relationships = {}
		self._right_of_relationships = {}

		if self._id in universe._ids_to_things:
			raise RuntimeError(f'{self._id} already exists in universe!')
		if self._name in universe._names_to_ids:
			raise ValueError(f'{self._name} already exists in universe!')

		universe._ids_to_things[self._id] = self
		universe._names_to_ids[self._name] = self._id
		universe._next_id += 1

	@property
	def universe(self):
		"""
		:rtype: Universe
		"""
		return self._universe

	@property
	def id(self):
		"""
		:rtype: int
		"""
		return self._id

	@property
	def name(self):
		"""
		:rtype: str
		"""
		return self._name

	@property
	def value(self):
		return self._value

	@property
	def relationships(self):
		"""
		:rtype: Relationship
		"""
		relationships = []

		for r in self._left_of_relationships.values():
			relationships.append(r)

		for r in self._middle_of_relationships.values():
			relationships.append(r)

		for r in self._right_of_relationships.values():
			relationships.append(r)

		return relationships

	def __str__(self):
		return self.name

	def __repr__(self):
		return f'{self.__class__.__name__} {self.id}: {self.name}'

	def __del__(self):
		self.universe.remove_thing(self.id)
		super().__del__()


class Relationship(Thing):
	def __init__(self, thing1, thing2, thing3):
		"""
		:type thing1: Thing
		:type thing2: Thing
		:type thing3: Thing
		"""
		universe = thing1.universe
		if universe != thing2.universe or universe != thing3.universe:
			raise RuntimeError('The things are not from the same universe!')
		super().__init__(universe=universe, name=f'{thing1.name}__{thing2.name}__{thing3.name}')
		self._thing1 = thing1
		self._thing2 = thing2
		self._thing3 = thing3

		if not thing1.id in self.universe._left_to_relationships:
			self.universe._left_to_relationships[thing1.id] = {}
		if not thing2.id in self.universe._middle_to_relationships:
			self.universe._middle_to_relationships[thing2.id] = {}
		if not thing3.id in self.universe._right_to_relationships:
			self.universe._right_to_relationships[thing3.id] = {}

		self.universe._left_to_relationships[thing1.id][self.id] = self
		self.universe._middle_to_relationships[thing2.id][self.id] = self
		self.universe._right_to_relationships[thing3.id][self.id] = self

		thing1._left_of_relationships[self.id] = self
		thing2._middle_of_relationships[self.id] = self
		thing3._right_of_relationships[self.id] = self
