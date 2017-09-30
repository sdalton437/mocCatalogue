from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Sport, Item, User

engine = create_engine('sqlite:///catalogitems.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Create dummy user
User1 = User(name="Robert Munch", email="rmunch@fake.com",
             picture='')
session.add(User1)
session.commit()

# Whitewater kayaking

sport1 = Sport(name='Whitewater Kayaking',
               picture='/static/img/whitewaterkayaking.jpg')

session.add(sport1)
session.commit()

item1 = Item(sport=sport1, name='Whitewater Paddle',
             description=('A paddle used to propel and maneuver'
                          ' whitewater kayaks. Primary use is for whitewater'),
             picture='/static/img/whitewaterpaddle.jpg', user_id=1)

session.add(item1)
session.commit()

item2 = Item(sport=sport1, name='Whitewater Sprayskirt',
             description=('A waterproof cover for a whitewater kayak,'
                          ' that prevents water from entering the'
                          ' boat while still '
                          'allowing the paddler to maneuver'),
             picture='/static/img/whitewaterkayakskirt.jpg', user_id=1)

session.add(item2)
session.commit()

item3 = Item(sport=sport1, name='Whitewater Kayak',
             description='A kayak meant to be used in whitewater',
             picture='/static/img/whitewaterkayak.jpg', user_id=1)

session.add(item3)
session.commit()


# Rock Climbing

sport2 = Sport(name='Rock Climbing', picture='/static/img/rockclimbing.jpg')

session.add(sport2)
session.commit()

item4 = Item(sport=sport2, name='Climbing Rope',
             description='Rope used for climbing',
             picture='/static/img/climbingrope.jpg', user_id=1)

session.add(item4)
session.commit()

item5 = Item(sport=sport2, name='Climbing Harness',
             description='Used to secure climber to rope',
             picture='/static/img/climbingharness.jpg', user_id=1)

session.add(item5)
session.commit()

item6 = Item(sport=sport2, name='Climbing Shoes',
             description='Shoes used for climbing',
             picture='/static/img/climbingshoes.jpg', user_id=1)

session.add(item6)
session.commit()

# Ice Climbing

sport3 = Sport(name='Ice Climbing', picture='/static/img/iceclimbing.jpg')

session.add(sport3)
session.commit()

item7 = Item(sport=sport3, name='Ice Tool',
             description='Tool used to ascend ice',
             picture='/static/img/iceclimbingicetool.jpg', user_id=1)

session.add(item7)
session.commit()

item8 = Item(sport=sport3, name='Ice Crampons',
             description='Crampons used for ice climbing',
             picture='/static/img/iceclimbingcrampons.jpg', user_id=1)

session.add(item8)
session.commit()

item9 = Item(sport=sport3, name='Mountainering Boots',
             description='Boots used for mountaineering sports',
             picture='/static/img/iceclimbingmountaineeringboots.jpg',
             user_id=1)

session.add(item9)
session.commit()

# Camping

sport4 = Sport(name='Camping', picture='/static/img/camping.jpg')

session.add(sport4)
session.commit()

item10 = Item(sport=sport4, name='Tent',
              description='Makeshift shelter used for the outdoors',
              picture='/static/img/campingtent.jpg', user_id=1)

session.add(item10)
session.commit()

item11 = Item(sport=sport4, name='Sleeping Bag',
              description='Bag used for sleeping in the wilderness',
              picture='/static/img/campingsleepingbag.jpg', user_id=1)

session.add(item11)
session.commit()

item12 = Item(sport=sport4, name='Sleeping Mat',
              description=('Mat used to seperate user from the bare'
                           ' ground while camping'),
              picture='/static/img/campingsleepingmat.jpg', user_id=1)

session.add(item12)
session.commit()


print "added catalogue items!"
