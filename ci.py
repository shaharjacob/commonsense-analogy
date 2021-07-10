import unittest
from pathlib import Path

import concept_net
import suggest_entities
import google_autosuggest
from quasimodo import Quasimodo, merge_tsvs


class TestFunctions(unittest.TestCase):

    def test_concept_net(self):
        # testing concept_net.get_entities_relations
        reference = ['revolving around the']
        actual = concept_net.get_entities_relations("earth", "sun")
        self.assertEqual(sorted(reference), sorted(actual))

        # testing concept_net.get_entity_props
        reference = ['4.5 billion years old', 'a word', 'an oblate sphereoid', 'an oblate spheroid', 'finite', 'flat', 'one astronomical unit from the Sun', 'one of many planets', 'receive rain from clouds', 'revolving around the sun', 'round like a ball', 'spherical', 'spherical in shape', 'very beautiful', 'very heavy']
        actual = concept_net.get_entity_props("earth", n_best=10)
        self.assertEqual(sorted(reference), sorted(actual))


    def test_google_autosuggest(self):
        # testing google_autosuggest.get_entities_relations
        # reference = ['revolve around', 'orbit', 'circle the', 'rotate around', 'move around the', 'spin around the', 'not fall into', 'move around']
        reference = ['revolve around', 'rotate around the', 'orbit', 'need the', 'rotate around', 'not collide with', 'orbit around the', 'spin around the', 'orbit the', 'start orbiting the', 'form after the formation of', 'from the formation of the']
        actual = google_autosuggest.get_entities_relations("earth", "sun").get("props")
        # the return values changed all the time, so we just check the API is not broken.
        self.assertTrue(set(reference) & set(actual))

        # testing google_autosuggest.get_entity_props
        reference = ['derived unit', 'fundamental unit', 'derived unit why', 'unit for measuring', 'unit of', 'fundamental unit or derived unit', 'measure of']
        actual = google_autosuggest.get_entity_props("newton")
        self.assertEqual(sorted(reference), sorted(actual))

        # testing google_autosuggest.get_entity_suggestions
        reference = ['edison', 'benjamin', 'faraday', 'they']
        actual = google_autosuggest.get_entity_suggestions("electricity", "discovered")
        self.assertEqual(sorted(reference), sorted(actual))


    def test_quasimodo(self):
        merge_tsvs(str(Path.cwd() / 'tsv' / 'quasimodo.tsv'))
        quasimodo = Quasimodo(path=str(Path.cwd() / 'tsv' / 'quasimodo.tsv'))
        
        # testing quasimodo.get_entity_props
        reference = ['has body part hoof', 'eat grass', 'has body part leg', 'need horseshoes', 'has body part nose']
        actual = [f"{prop[0]} {prop[1]}" for prop in quasimodo.get_entity_props('horse', n_largest=5, plural_and_singular=True)]
        self.assertEqual(sorted(reference), sorted(actual))
        
        # testing quasimodo.get_entities_relations
        reference = ['be to', 'rotate around', 'pull in', 'orbit', 'be closest star to']
        actual = quasimodo.get_entities_relations('sun', 'earth', n_largest=5, plural_and_singular=True)
        self.assertEqual(sorted(reference), sorted(actual))

        # testing quasimodo.get_similarity_between_entities
        reference = ['has temperature hot', 'has property aesthetic', 'has color blue', 'be in space', 'has property round']
        actual = [f"{prop[0]} {prop[1]}" for prop in quasimodo.get_similarity_between_entities('sun', 'earth', n_largest=5, plural_and_singular=True)]
        self.assertEqual(sorted(reference), sorted(actual))
    

    def test_suggest_entities(self):
        # testing get_score_between_two_entitites
        reference = 0.83
        actual = suggest_entities.get_score_between_two_entitites("newton", "faraday")
        self.assertEqual(reference, actual)

        # testing get_best_matches_for_entity
        reference = [('newton', 'faraday', 0.83), ('newton', 'paper', 0.483), ('newton', 'wall', 0.482), ('newton', 'apple', 0.438), ('newton', 'tomato', 0.437)]
        actual = suggest_entities.get_best_matches_for_entity("newton", ["faraday", "sky", "window", "paper", "photo", "apple", "tomato", "wall", "home", "horse"])
        self.assertEqual(reference, actual)


if __name__ == '__main__':
    unittest.main()
