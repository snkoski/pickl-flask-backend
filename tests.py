import unittest

from app import app, db
from config import Config
from app.models import Team, Game, User, Vote

class TeamModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_team(self):
        team1 = Team(name='Yankees', city='New York', abbreviation='NYY')
        team2 = Team(name='Cubs', city='Chicago', abbreviation='CHC')
        db.session.add(team1)
        db.session.add(team2)
        db.session.commit()
        self.assertEqual(team1.name, 'Yankees')
        self.assertEqual(team1.city, 'New York')
        self.assertEqual(team1.abbreviation, 'NYY')
        self.assertEqual(team2.name, 'Cubs')
        self.assertEqual(team2.city, 'Chicago')
        self.assertEqual(team2.abbreviation, 'CHC')
    
    def test_game(self):
        team1 = Team(name='Yankees', city='New York', abbreviation='NYY')
        team2 = Team(name='Cubs', city='Chicago', abbreviation='CHC')
        game1 = Game(schedule_status='normal', 
                     delayed_or_postponed_reason=None, 
                     location='Yankee Stadium', 
                     home_team=team1, 
                     away_team=team2
        )
        db.session.add_all([team1, team2, game1])
        db.session.commit()
        self.assertEqual(game1.schedule_status, 'normal')
        self.assertEqual(game1.location, 'Yankee Stadium')
        self.assertEqual(game1.delayed_or_postponed_reason, None)
        
        self.assertEqual(game1.home_team.name, 'Yankees')
        self.assertEqual(len(team1.home_games), 1)

        game2 = Game(schedule_status='normal', 
                     delayed_or_postponed_reason=None, 
                     location='Yankee Stadium', 
                     home_team=team1, 
                     away_team=team2
        )
        game3 = Game(schedule_status='normal', 
                     delayed_or_postponed_reason=None, 
                     location='Wrigley Field', 
                     home_team=team2, 
                     away_team=team1
        )
        db.session.add_all([game2, game3])
        db.session.commit()
        self.assertEqual(len(team1.home_games), 2)
        self.assertEqual(len(team1.away_games), 1)

        game2.schedule_status = 'postponed'
        game2.delayed_or_postponed_reason = 'rain'

        self.assertEqual(game2.schedule_status, 'postponed')
        self.assertEqual(game2.delayed_or_postponed_reason, 'rain')

    def test_user(self):
        user1 = User(username='shawn', email='fake@email.com')
        db.session.add(user1)
        db.session.commit()
        self.assertEqual(user1.username, 'shawn')
        self.assertEqual(user1.email, 'fake@email.com')

    def test_vote(self):
        user1 = User(username='shawn', email='fake@email.com')
        team1 = Team(name='Yankees', city='New York', abbreviation='NYY')
        team2 = Team(name='Cubs', city='Chicago', abbreviation='CHC')
        game1 = Game(schedule_status='normal', 
                     delayed_or_postponed_reason=None, 
                     location='Yankee Stadium', 
                     home_team=team1, 
                     away_team=team2
        )
        # vote1 = Vote(voter=user1, game=game1, team=team1)
        db.session.add_all([user1, team1, team2, game1])
        db.session.commit()
        # self.assertEqual(vote1.voter, user1)
        # self.assertEqual(vote1.team.name, 'Yankees')
        # self.assertEqual(vote1.game.location, 'Yankee Stadium')
        # self.assertEqual(vote1.game.away_team.name, 'Cubs')

        user1.vote_for_team(game1, team2)
        self.assertEqual(team2.total_votes, 1)

        # new_vote = Vote(user_id=user1.id, game_id=game1.id, team_id=team1.id)
        # db.session.add(new_vote)
        # db.session.commit()
        # print(new_vote.voter)
        # self.assertEqual(new_vote.voter, user1)
        # self.assertEqual(new_vote.game, game1)
        # self.assertEqual(new_vote.team, team1)
        print(f'BEFORE CLASS METH {user1.total_votes}')
        Vote.place_vote(user1, game1, team2)
        self.assertEqual(team2.total_votes, 2)




    def test_add_remove_vote(self):
        team1 = Team(name='Yankees', city='New York', abbreviation='NYY')
        db.session.add(team1)
        db.session.commit()
        self.assertEqual(team1.total_votes, 0)
        self.assertEqual(team1.name, 'Yankees')

        team1.add_vote()
        team1.add_vote()
        team1.add_vote()
        self.assertEqual(team1.total_votes, 3)

        team1.remove_vote()     
        team1.remove_vote()
        team1.remove_vote()
        self.assertEqual(team1.total_votes, 0)

        team1.remove_vote()
        self.assertEqual(team1.total_votes, 0)



    

if __name__ == '__main__':
    unittest.main(verbosity=2)
