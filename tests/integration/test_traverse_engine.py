import pytest
from hyperon_das_atomdb import AtomDB, AtomDoesNotExist

from hyperon_das.das import DistributedAtomSpace

from .remote_das_info import remote_das_host, remote_das_port

human = AtomDB.node_handle('Concept', 'human')
monkey = AtomDB.node_handle('Concept', 'monkey')
chimp = AtomDB.node_handle('Concept', 'chimp')
mammal = AtomDB.node_handle('Concept', 'mammal')
ent = AtomDB.node_handle('Concept', 'ent')
animal = AtomDB.node_handle('Concept', 'animal')
reptile = AtomDB.node_handle('Concept', 'reptile')
dinosaur = AtomDB.node_handle('Concept', 'dinosaur')
triceratops = AtomDB.node_handle('Concept', 'triceratops')
rhino = AtomDB.node_handle('Concept', 'rhino')
earthworm = AtomDB.node_handle('Concept', 'earthworm')
snake = AtomDB.node_handle('Concept', 'snake')
vine = AtomDB.node_handle('Concept', 'vine')
plant = AtomDB.node_handle('Concept', 'plant')

similarity_human_monkey = AtomDB.link_handle('Similarity', [human, monkey])
similarity_human_chimp = AtomDB.link_handle('Similarity', [human, chimp])
similarity_chimp_monkey = AtomDB.link_handle('Similarity', [chimp, monkey])
similarity_snake_earthworm = AtomDB.link_handle('Similarity', [snake, earthworm])
similarity_rhino_triceratops = AtomDB.link_handle('Similarity', [rhino, triceratops])
similarity_snake_vine = AtomDB.link_handle('Similarity', [snake, vine])
similarity_human_ent = AtomDB.link_handle('Similarity', [human, ent])
inheritance_human_mammal = AtomDB.link_handle('Inheritance', [human, mammal])
inheritance_monkey_mammal = AtomDB.link_handle('Inheritance', [monkey, mammal])
inheritance_chimp_mammal = AtomDB.link_handle('Inheritance', [chimp, mammal])
inheritance_mammal_animal = AtomDB.link_handle('Inheritance', [mammal, animal])
inheritance_reptile_animal = AtomDB.link_handle('Inheritance', [reptile, animal])
inheritance_snake_reptile = AtomDB.link_handle('Inheritance', [snake, reptile])
inheritance_dinosaur_reptile = AtomDB.link_handle('Inheritance', [dinosaur, reptile])
inheritance_triceratops_dinosaur = AtomDB.link_handle('Inheritance', [triceratops, dinosaur])
inheritance_earthworm_animal = AtomDB.link_handle('Inheritance', [earthworm, animal])
inheritance_rhino_mammal = AtomDB.link_handle('Inheritance', [rhino, mammal])
inheritance_vine_plant = AtomDB.link_handle('Inheritance', [vine, plant])
inheritance_ent_plant = AtomDB.link_handle('Inheritance', [ent, plant])
similarity_monkey_human = AtomDB.link_handle('Similarity', [monkey, human])
similarity_chimp_human = AtomDB.link_handle('Similarity', [chimp, human])
similarity_monkey_chimp = AtomDB.link_handle('Similarity', [monkey, chimp])
similarity_earthworm_snake = AtomDB.link_handle('Similarity', [earthworm, snake])
similarity_triceratops_rhino = AtomDB.link_handle('Similarity', [triceratops, rhino])
similarity_vine_snake = AtomDB.link_handle('Similarity', [vine, snake])
similarity_ent_human = AtomDB.link_handle('Similarity', [ent, human])


class TestTraverseEngine:
    def test_traverse_engine_remote(self):
        """Test TraverseEngine methods with remote DAS in OpenFaas"""

        def get():
            das = DistributedAtomSpace(
                query_engine='remote', host=remote_das_host, port=remote_das_port
            )
            cursor = das.get_traversal_cursor(human)
            current_cursor = cursor.get()

            assert current_cursor['handle'] == human
            assert current_cursor['name'] == 'human'
            assert current_cursor['named_type'] == 'Concept'

        def get_links():
            das = DistributedAtomSpace(
                query_engine='remote', host=remote_das_host, port=remote_das_port
            )

            def _build_atom_answer(handle: str) -> dict:
                cursor = das.get_traversal_cursor(handle)
                links = cursor.get_links()
                return sorted([link['handle'] for link in links])

            def _human_links():
                answers = _build_atom_answer(human)
                assert len(answers) == 7
                assert answers == sorted(
                    [
                        similarity_human_chimp,
                        similarity_human_monkey,
                        similarity_human_ent,
                        similarity_ent_human,
                        similarity_monkey_human,
                        similarity_chimp_human,
                        inheritance_human_mammal,
                    ]
                )

            def _chimp_links():
                answers = _build_atom_answer(chimp)
                assert len(answers) == 5
                assert answers == sorted(
                    [
                        inheritance_chimp_mammal,
                        similarity_monkey_chimp,
                        similarity_chimp_monkey,
                        similarity_chimp_human,
                        similarity_human_chimp,
                    ]
                )

            def _ent_links():
                answers = _build_atom_answer(ent)
                assert len(answers) == 3
                assert answers == sorted(
                    [inheritance_ent_plant, similarity_human_ent, similarity_ent_human]
                )

            def _similarity_links():
                answers = _build_atom_answer(similarity_human_chimp)
                assert len(answers) == 0

                answers = _build_atom_answer(similarity_chimp_monkey)
                assert len(answers) == 0

                answers = _build_atom_answer(similarity_human_ent)
                assert len(answers) == 0

            _human_links()

            _chimp_links()

            _ent_links()

            _similarity_links()

        def get_links_with_filters():
            das = DistributedAtomSpace(
                query_engine='remote', host=remote_das_host, port=remote_das_port
            )

            def _build_atom_answer(handle: str, **filters) -> dict:
                cursor = das.get_traversal_cursor(handle)
                links = cursor.get_links(**filters)
                return sorted([link['handle'] for link in links])

            def _human_links():
                answers = _build_atom_answer(human, link_type='Similarity')
                assert answers == sorted(
                    [
                        similarity_human_chimp,
                        similarity_human_monkey,
                        similarity_human_ent,
                        similarity_ent_human,
                        similarity_monkey_human,
                        similarity_chimp_human,
                    ]
                )

                answers = _build_atom_answer(human, link_type='Similarity', cursor_position=0)
                assert answers == sorted(
                    [similarity_human_chimp, similarity_human_monkey, similarity_human_ent]
                )

                answers = _build_atom_answer(human, link_type='Similarity', cursor_position=1)
                assert answers == sorted(
                    [similarity_ent_human, similarity_monkey_human, similarity_chimp_human]
                )

                answers = _build_atom_answer(
                    human, link_type='Similarity', cursor_position=0, target_type='Concept'
                )
                assert answers == sorted(
                    [
                        similarity_human_chimp,
                        similarity_human_monkey,
                        similarity_human_ent,
                    ]
                )
                answers = _build_atom_answer(human, link_type='Fake')
                assert len(answers) == 0
                answers = _build_atom_answer(human, cursor_position=2)
                assert len(answers) == 0
                answers = _build_atom_answer(human, target_type='Fake')
                assert len(answers) == 0

                das.add_link(
                    {
                        'type': 'Similarity',
                        'targets': [
                            {'type': 'Concept', 'name': 'human'},
                            {'type': 'Concept', 'name': 'snet'},
                        ],
                        'weight': 0.5,
                    }
                )

                def my_filter(link) -> bool:
                    if 'weight' in link:
                        return True
                    return False

                answers = _build_atom_answer(
                    human,
                    link_type='Similarity',
                    cursor_position=0,
                    target_type='Concept',
                    filter=my_filter,
                )
                assert answers == [
                    AtomDB.link_handle('Similarity', [human, AtomDB.node_handle('Concept', 'snet')])
                ]

                def my_second_filter(link):
                    if 'weight' in link and link['weight'] >= 0.5:
                        return link

                with pytest.raises(TypeError) as exc:
                    _build_atom_answer(human, filter=my_second_filter)
                assert exc.value.args[0] == 'The function must return a boolean'

            def _mammal_links():
                answers = _build_atom_answer(mammal, link_type='Inheritance')
                assert answers == sorted(
                    [
                        inheritance_mammal_animal,
                        inheritance_monkey_mammal,
                        inheritance_chimp_mammal,
                        inheritance_human_mammal,
                        inheritance_rhino_mammal,
                    ]
                )
                answers = _build_atom_answer(mammal, link_type='Inheritance', cursor_position=0)
                assert answers == sorted([inheritance_mammal_animal])
                answers = _build_atom_answer(mammal, link_type='Inheritance', cursor_position=1)
                assert answers == sorted(
                    [
                        inheritance_monkey_mammal,
                        inheritance_chimp_mammal,
                        inheritance_human_mammal,
                        inheritance_rhino_mammal,
                    ]
                )
                answers = _build_atom_answer(
                    mammal, link_type='Inheritance', cursor_position=1, target_type='Concept'
                )
                assert answers == sorted(
                    [
                        inheritance_monkey_mammal,
                        inheritance_chimp_mammal,
                        inheritance_human_mammal,
                        inheritance_rhino_mammal,
                    ]
                )
                answers = _build_atom_answer(mammal, link_type='Similarity')
                assert len(answers) == 0
                answers = _build_atom_answer(mammal, cursor_position=5)
                assert len(answers) == 0
                answers = _build_atom_answer(mammal, target_type='Snet')
                assert len(answers) == 0

                das.add_link(
                    {
                        'type': 'Inheritance',
                        'targets': [
                            {'type': 'Fake', 'name': 'fake1'},
                            {'type': 'Concept', 'name': 'mammal'},
                        ],
                        'weight': 0.4,
                    }
                )
                das.add_link(
                    {
                        'type': 'Inheritance',
                        'targets': [
                            {'type': 'Fake', 'name': 'fake2'},
                            {'type': 'Concept', 'name': 'mammal'},
                        ],
                        'weight': 0.5,
                    }
                )

                def my_filter(link) -> bool:
                    if 'weight' in link and link['weight'] >= 0.5:
                        return True
                    return False

                answers = _build_atom_answer(
                    mammal,
                    link_type='Inheritance',
                    cursor_position=1,
                    target_type='Fake',
                    filter=my_filter,
                )
                assert answers == [
                    AtomDB.link_handle('Inheritance', [AtomDB.node_handle('Fake', 'fake2'), mammal])
                ]

            def _snake_links():
                answers = _build_atom_answer(snake, link_type='Similarity')
                assert answers == sorted(
                    [
                        similarity_snake_earthworm,
                        similarity_earthworm_snake,
                        similarity_snake_vine,
                        similarity_vine_snake,
                    ]
                )
                answers = _build_atom_answer(snake, link_type='Inheritance', cursor_position=0)
                assert answers == sorted(
                    [
                        inheritance_snake_reptile,
                    ]
                )
                answers = _build_atom_answer(snake, link_type='Inheritance', cursor_position=1)
                assert len(answers) == 0
                answers = _build_atom_answer(snake, link_type='Similarity', cursor_position=0)
                assert answers == sorted(
                    [
                        similarity_snake_earthworm,
                        similarity_snake_vine,
                    ]
                )
                answers = _build_atom_answer(snake, link_type='Similarity', cursor_position=1)
                assert answers == sorted(
                    [
                        similarity_earthworm_snake,
                        similarity_vine_snake,
                    ]
                )
                answers = _build_atom_answer(
                    snake, link_type='Inheritance', cursor_position=0, target_type='Concept'
                )
                assert answers == sorted([inheritance_snake_reptile])
                answers = _build_atom_answer(snake, link_type='Evaluation')
                assert len(answers) == 0
                answers = _build_atom_answer(snake, cursor_position=5)
                assert len(answers) == 0
                answers = _build_atom_answer(
                    snake, link_type='Inheritance', cursor_position=0, target_type='Snet'
                )
                assert len(answers) == 0

                das.add_link(
                    {
                        'type': 'Similarity',
                        'targets': [
                            {'type': 'Fake', 'name': 'fake1'},
                            {'type': 'Concept', 'name': 'snake'},
                        ],
                        'weight': 0.2,
                    }
                )
                das.add_link(
                    {
                        'type': 'Similarity',
                        'targets': [
                            {'type': 'Concept', 'name': 'snake'},
                            {'type': 'Fake', 'name': 'fake1'},
                        ],
                        'weight': 0.5,
                    }
                )

                def my_filter(link) -> bool:
                    if 'weight' in link and link['weight'] >= 0.5:
                        return True
                    return False

                answers = _build_atom_answer(
                    snake, link_type='Similarity', target_type='Fake', filter=my_filter
                )
                assert answers == [
                    AtomDB.link_handle("Similarity", [snake, AtomDB.node_handle('Fake', 'fake1')])
                ]

            def _similarity_human_monkey_links():
                answers = _build_atom_answer(similarity_human_monkey, link_type='Similarity')
                assert len(answers) == 0

                das.add_link(
                    {
                        'type': 'Inheritance',
                        'targets': [
                            {'type': 'Fake', 'name': 'fake'},
                            {
                                'type': 'Similarity',
                                'targets': [
                                    {'type': 'Concept', 'name': 'human'},
                                    {'type': 'Concept', 'name': 'monkey'},
                                ],
                            },
                        ],
                    }
                )

                cursor = das.get_traversal_cursor(similarity_human_monkey)
                links = cursor.get_links(link_type='Inheritance')
                answers = [link for link in links]
                assert len(answers) == 1

            _human_links()
            _mammal_links()
            _snake_links()
            _similarity_human_monkey_links()

        def get_neighbors():
            das = DistributedAtomSpace(
                query_engine='remote', host=remote_das_host, port=remote_das_port
            )

            def _build_neighbors(handle: str) -> dict:
                cursor = das.get_traversal_cursor(handle)
                neighbors_iterator = cursor.get_neighbors()
                return [item for item in neighbors_iterator]

            def _monkey_neighbors():
                neighbors = _build_neighbors(monkey)
                assert das.get_atom(human) in neighbors
                assert das.get_atom(mammal) in neighbors
                assert das.get_atom(chimp) in neighbors
                assert len(neighbors) == 3

            def _dinosaur_neighbors():
                neighbors = _build_neighbors(dinosaur)
                assert das.get_atom(reptile) in neighbors
                assert das.get_atom(triceratops) in neighbors
                assert len(neighbors) == 2

            def _rhino_neighbors():
                neighbors = _build_neighbors(rhino)
                assert das.get_atom(mammal) in neighbors
                assert das.get_atom(triceratops) in neighbors
                assert len(neighbors) == 2

            def _inheritance_neighbors():
                answers = _build_neighbors(inheritance_monkey_mammal)
                assert len(answers) == 0

                answers = _build_neighbors(inheritance_dinosaur_reptile)
                assert len(answers) == 0

                answers = _build_neighbors(inheritance_rhino_mammal)
                assert len(answers) == 0

            _monkey_neighbors()

            _dinosaur_neighbors()

            _rhino_neighbors()

            _inheritance_neighbors()

        def get_neighbors_with_filters():
            das = DistributedAtomSpace(
                query_engine='remote', host=remote_das_host, port=remote_das_port
            )

            def _build_neighbors(handle: str, **filters) -> dict:
                cursor = das.get_traversal_cursor(handle)
                neighbors_iterator = cursor.get_neighbors(**filters)
                ret = []
                for item in neighbors_iterator:
                    ret.append(item)
                return ret

            def _human_neighbors():
                neighbors = _build_neighbors(human, link_type='Inheritance')
                assert das.get_atom(mammal) in neighbors
                assert len(neighbors) == 1

                neighbors = _build_neighbors(human, link_type='Similarity')
                assert das.get_atom(monkey) in neighbors
                assert das.get_atom(chimp) in neighbors
                assert das.get_atom(ent) in neighbors
                assert len(neighbors) == 3

                neighbors = _build_neighbors(human, target_type='Concept')
                assert das.get_atom(mammal) in neighbors
                assert das.get_atom(monkey) in neighbors
                assert das.get_atom(chimp) in neighbors
                assert das.get_atom(ent) in neighbors
                assert len(neighbors) == 4

                neighbors = _build_neighbors(human, link_type='Inheritance', target_type='Snet')
                assert len(neighbors) == 0

                neighbors = _build_neighbors(human, link_type='Similarity', target_type='Snet')
                assert len(neighbors) == 0

                das.add_link(
                    {
                        'type': 'Similarity',
                        'targets': [
                            {'type': 'Concept', 'name': 'human'},
                            {'type': 'Fake', 'name': 'fake-h'},
                        ],
                        'weight': 0.7,
                    }
                )
                das.add_link(
                    {
                        'type': 'Similarity',
                        'targets': [
                            {'type': 'Fake', 'name': 'fake-h'},
                            {'type': 'Concept', 'name': 'human'},
                        ],
                        'weight': 0.3,
                    }
                )
                das.add_link(
                    {
                        'type': 'Inheritance',
                        'targets': [
                            {'type': 'Fake', 'name': 'fake-h2'},
                            {'type': 'Fake', 'name': 'fake-h3'},
                            {'type': 'Fake', 'name': 'fake-h4'},
                            {'type': 'Concept', 'name': 'human'},
                        ],
                        'weight': 0.3,
                    }
                )

                def my_filter(link) -> bool:
                    if 'weight' in link and link['weight'] >= 1:
                        return True
                    return False

                fake_h = AtomDB.node_handle('Fake', 'fake-h')
                fake_h2 = AtomDB.node_handle('Fake', 'fake-h2')
                fake_h3 = AtomDB.node_handle('Fake', 'fake-h3')
                fake_h4 = AtomDB.node_handle('Fake', 'fake-h4')

                neighbors = _build_neighbors(human)
                assert das.get_atom(mammal) in neighbors
                assert das.get_atom(monkey) in neighbors
                assert das.get_atom(chimp) in neighbors
                assert das.get_atom(ent) in neighbors
                assert das.get_atom(fake_h) in neighbors
                assert das.get_atom(fake_h2) in neighbors
                assert das.get_atom(fake_h3) in neighbors
                assert das.get_atom(fake_h4) in neighbors
                assert len(neighbors) == 8

                neighbors = _build_neighbors(human, link_type='Similarity', target_type='Fake')
                assert das.get_atom(fake_h) in neighbors
                assert len(neighbors) == 1

                neighbors = _build_neighbors(
                    human, link_type='Similarity', target_type='Fake', filter=my_filter
                )
                assert len(neighbors) == 0

            def _vine_neighbors():
                neighbors = _build_neighbors(vine, link_type='Similarity')
                assert das.get_atom(snake) in neighbors
                assert len(neighbors) == 1

                neighbors = _build_neighbors(vine, link_type='Inheritance')
                assert das.get_atom(plant) in neighbors
                assert len(neighbors) == 1

                fake_v1 = AtomDB.node_handle('Fake', 'fake-v1')
                fake_v2 = AtomDB.node_handle('Fake', 'fake-v2')

                das.add_link(
                    {
                        'type': 'Inheritance',
                        'targets': [
                            {'type': 'Fake', 'name': 'fake-v1'},
                            {'type': 'Concept', 'name': 'vine'},
                        ],
                        'weight': 1,
                    }
                )
                das.add_link(
                    {
                        'type': 'Similarity',
                        'targets': [
                            {'type': 'Concept', 'name': 'vine'},
                            {'type': 'Fake', 'name': 'fake-v2'},
                        ],
                        'weight': 0.7,
                    }
                )
                das.add_link(
                    {
                        'type': 'Similarity',
                        'targets': [
                            {'type': 'Fake', 'name': 'fake-v2'},
                            {'type': 'Concept', 'name': 'vine'},
                        ],
                        'weight': 0.3,
                    }
                )

                neighbors = _build_neighbors(vine, link_type='Inheritance')
                assert das.get_atom(plant) in neighbors
                assert das.get_atom(fake_v1) in neighbors
                assert len(neighbors) == 2

                neighbors = _build_neighbors(vine, link_type='Similarity')
                assert das.get_atom(snake) in neighbors
                assert das.get_atom(fake_v2) in neighbors
                assert len(neighbors) == 2

                neighbors = _build_neighbors(vine, link_type='Similarity', target_type='Concept')
                assert das.get_atom(snake) in neighbors
                assert len(neighbors) == 1

                neighbors = _build_neighbors(vine, link_type='Inheritance', target_type='Fake')
                assert das.get_atom(fake_v1) in neighbors
                assert len(neighbors) == 1

                neighbors = _build_neighbors(vine, link_type='Similarity', target_type='Fake')
                assert das.get_atom(fake_v2) in neighbors
                assert len(neighbors) == 1

                def my_filter(link) -> bool:
                    if 'weight' in link and link['weight'] >= 1:
                        return True
                    return False

                neighbors = _build_neighbors(vine, link_type='Similarity', filter=my_filter)
                assert len(neighbors) == 0

                neighbors = _build_neighbors(vine, link_type='Inheritance', filter=my_filter)
                assert das.get_atom(fake_v1) in neighbors
                assert len(neighbors) == 1

            def _inheritance_dinosaur_reptile():
                neighbors = _build_neighbors(inheritance_dinosaur_reptile)
                assert len(neighbors) == 0

                fake_dr1 = AtomDB.node_handle('Fake', 'fake-dr1')
                fake_dr2 = AtomDB.node_handle('Fake', 'fake-dr2')

                das.add_link(
                    {
                        'type': 'Inheritance',
                        'targets': [
                            {'type': 'Fake', 'name': 'fake-dr1'},
                            {
                                'type': 'Inheritance',
                                'targets': [
                                    {'type': 'Concept', 'name': 'dinosaur'},
                                    {'type': 'Concept', 'name': 'reptile'},
                                ],
                            },
                        ],
                        'weight': 1,
                    }
                )
                das.add_link(
                    {
                        'type': 'Similarity',
                        'targets': [
                            {
                                'type': 'Inheritance',
                                'targets': [
                                    {'type': 'Concept', 'name': 'dinosaur'},
                                    {'type': 'Concept', 'name': 'reptile'},
                                ],
                            },
                            {'type': 'Fake', 'name': 'fake-dr2'},
                        ],
                        'weight': 0.7,
                    }
                )
                das.add_link(
                    {
                        'type': 'Similarity',
                        'targets': [
                            {'type': 'Fake', 'name': 'fake-dr2'},
                            {
                                'type': 'Inheritance',
                                'targets': [
                                    {'type': 'Concept', 'name': 'dinosaur'},
                                    {'type': 'Concept', 'name': 'reptile'},
                                ],
                            },
                        ],
                        'weight': 0.3,
                    }
                )

                neighbors = _build_neighbors(inheritance_dinosaur_reptile)
                assert das.get_atom(fake_dr1) in neighbors
                assert das.get_atom(fake_dr2) in neighbors
                assert len(neighbors) == 2

                neighbors = _build_neighbors(inheritance_dinosaur_reptile, link_type='Similarity')
                assert das.get_atom(fake_dr2) in neighbors
                assert len(neighbors) == 1

                neighbors = _build_neighbors(inheritance_dinosaur_reptile, link_type='Inheritance')
                assert das.get_atom(fake_dr1) in neighbors
                assert len(neighbors) == 1

                neighbors = _build_neighbors(
                    inheritance_dinosaur_reptile, link_type='Inheritance', target_type='Fake'
                )
                assert das.get_atom(fake_dr1) in neighbors
                assert len(neighbors) == 1

                neighbors = _build_neighbors(
                    inheritance_dinosaur_reptile, link_type='Inheritance', target_type='Concept'
                )
                assert len(neighbors) == 0

                neighbors = _build_neighbors(inheritance_dinosaur_reptile, target_type='Concept')
                assert len(neighbors) == 0

                neighbors = _build_neighbors(inheritance_dinosaur_reptile, target_type='Fake')
                assert das.get_atom(fake_dr1) in neighbors
                assert das.get_atom(fake_dr2) in neighbors
                assert len(neighbors) == 2

            _human_neighbors()
            _vine_neighbors()
            _inheritance_dinosaur_reptile()

        def follow_link():
            das = DistributedAtomSpace(
                query_engine='remote', host=remote_das_host, port=remote_das_port
            )

            def _mammal():
                cursor = das.get_traversal_cursor(mammal)
                assert cursor.get()['name'] == 'mammal'

                cursor.follow_link()
                current_cursor = cursor.get()['name']
                assert current_cursor in ('monkey', 'chimp', 'human', 'animal', 'rhino')

                cursor.follow_link()
                previous_cursor = current_cursor
                current_cursor = cursor.get()['name']
                if previous_cursor == 'monkey':
                    assert current_cursor in ('mammal', 'chimp', 'human')
                elif previous_cursor == 'chimp':
                    assert current_cursor in ('mammal', 'monkey', 'human')
                elif previous_cursor == 'human':
                    assert current_cursor in ('mammal', 'monkey', 'chimp', 'ent')
                elif previous_cursor == 'animal':
                    assert current_cursor in ('mammal', 'reptile', 'earthworm')
                elif previous_cursor == 'rhino':
                    assert current_cursor in ('mammal', 'triceratops')

            def _earthworm():
                cursor = das.get_traversal_cursor(earthworm)
                assert cursor.get()['name'] == 'earthworm'

                cursor.follow_link()
                current_cursor = cursor.get()['name']
                assert current_cursor in ('animal', 'snake')

                cursor.follow_link()
                previous_cursor = current_cursor
                current_cursor = cursor.get()['name']

                if previous_cursor == 'animal':
                    assert current_cursor in ('mammal', 'reptile', 'earthworm')
                elif previous_cursor == 'snake':
                    assert current_cursor in ('earthworm', 'reptile', 'vine')

            _mammal()
            _earthworm()

        def follow_link_with_filters():
            das = DistributedAtomSpace(
                query_engine='remote', host=remote_das_host, port=remote_das_port
            )

            def _mammal():
                cursor = das.get_traversal_cursor(mammal)
                assert cursor.get()['name'] == 'mammal'

                cursor.follow_link(link_type='Similarity')
                assert cursor.get()['name'] == 'mammal'

                cursor.follow_link(link_type='Inheritance')
                current_cursor = cursor.get()['name']
                assert current_cursor in ('monkey', 'chimp', 'human', 'animal', 'rhino')

                cursor.follow_link(link_type='Inheritance', target_type='Concept')
                previous_cursor = current_cursor
                current_cursor = cursor.get()['name']
                if previous_cursor == 'monkey':
                    assert current_cursor in ('mammal', 'chimp')
                elif previous_cursor == 'chimp':
                    assert current_cursor in ('mammal', 'monkey', 'human')
                elif previous_cursor == 'human':
                    assert current_cursor in ('mammal', 'monkey', 'chimp', 'ent')
                elif previous_cursor == 'animal':
                    assert current_cursor in ('mammal', 'reptile', 'earthworm')
                elif previous_cursor == 'rhino':
                    assert current_cursor in ('mammal', 'triceratops')

                cursor.follow_link(link_type='Inheritance', target_type='Fake')
                previous_cursor = current_cursor
                current_cursor = cursor.get()['name']
                assert previous_cursor == current_cursor

            _mammal()

        def goto():
            das = DistributedAtomSpace(
                query_engine='remote', host=remote_das_host, port=remote_das_port
            )
            cursor = das.get_traversal_cursor(human)
            cursor.get()['name'] == 'human'

            cursor.goto(ent)
            assert cursor.get()['name'] == 'ent'

            with pytest.raises(AtomDoesNotExist):
                cursor.goto('snet')

        get()
        get_links()
        get_links_with_filters()
        get_neighbors()
        get_neighbors_with_filters()
        follow_link()
        follow_link_with_filters()
        goto()
