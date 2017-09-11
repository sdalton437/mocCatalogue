from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Sport, Item

engine = create_engine('sqlite:///catalogitems.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

sport1 = Sport(name = 'Whitewater Kayaking')

session.add(sport1)
session.commit()

item1 = Item(sport = sport1, name = 'Whitewater Paddle', description = 'A paddle used to propel and maneuver whitewater kayaks. Primary use is for whitewater')

session.add(item1)
session.commit()

item2 = Item(sport = sport1, name = 'Whitewater Sprayskirt', description = 'A waterproof cover for a whitewater kayak, that prevents water from entering the boat while still allowing the paddler to maneuver')

session.add(item2)
session.commit()

item3 = Item(sport = sport1, name = 'Whitewater Kayak', description = 'A kayak meant to be used in whitewater')

session.add(item3)
session.commit()

sport2 = Sport(name = 'Rock Climbing')

session.add(sport2)
session.commit()

item4 = Item(sport = sport2, name = 'Climbing Rope', description = 'Rope used for climbing')

session.add(item4)
session.commit()

item5 = Item(sport = sport2, name = 'Climbing Harness', description = 'Used to secure climber to rope')

session.add(item5)
session.commit()

item6 = Item(sport = sport2, name = 'Climbing Shoes', description = 'Shoes used for climbing')

session.add(item6)
session.commit()

sport3 = Sport(name = 'Ice Climbing')

session.add(sport3)
session.commit()

item7 = Item(sport = sport3, name = 'Ice Tool', description = 'Tool used to ascend ice')

session.add(item7)
session.commit()

item8 = Item(sport = sport3, name = 'Ice Crampons', description = 'Crampons used for ice climbing')

session.add(item8)
session.commit()

item9 = Item(sport = sport3, name = 'Mountainering Boots', description = 'Boots used for mountaineering sports')

session.add(item9)
session.commit()

sport4 = Sport(name = 'Camping')

session.add(sport4)
session.commit()

item10 = Item(sport = sport4, name = 'Tent', description = 'Makeshift shelter used for the outdoors')

session.add(item10)
session.commit()

item11 = Item(sport = sport4, name = 'Sleeping Bag', description = 'Bag used for sleeping in the wilderness')

session.add(item11)
session.commit()

item12 = Item(sport = sport4, name = 'Sleeping Mat', description = 'Mat used to seperate user from the bare ground while camping')

session.add(item12)
session.commit()


print "added menu items!"


