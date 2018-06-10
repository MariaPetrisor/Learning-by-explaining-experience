#!/usr/bin/python2.7

'''
    File name: explaining_experience_learning.py 
    Author: Maria Petrisor
    Date created: 27/05/2018
    Python Version: 2.7
'''


class Link:
    def __init__(self, link_type, str1, str2):
        self.link_type = link_type
        self.str1 = str1
        self.str2 = str2

    def get_string_tuple(self):
        return (self.str1, self.str2)

    def get_link_type(self):
        return self.link_type

    def compare_links(self, new_link):
        return new_link.get_link_type() == self.link_type and new_link.get_string_tuple() == (self.str1, self.str2)

    def to_string(self):
        return "{}({}, {})".format(self.link_type, self.str1, self.str2)


class Implies:
    def __init__(self, rules_list, consequence):
        self.rules_list = rules_list
        self.consequence = consequence

    def get_rules_list(self):
        return self.rules_list

    def get_consequence(self):
        return self.consequence


class Description:
    def __init__(self, link_list, implies_list):
        self.link_list = link_list
        self.implies_list = implies_list
        self.deducted_properties = []

    def get_link_list(self):
        return self.link_list

    def get_implies_list(self):
        return self.implies_list

    def get_deducted_properties(self):
        return self.deducted_properties

    def add_deducted_property(self, property):
        self.deducted_properties.append(property)


class Model:
    def __init__(self, object_description, unclassified_object, precedents_list, link_to_demonstrate):
        self.object_description = object_description
        self.unclassified_object = unclassified_object
        self.precedents_list = precedents_list
        self.link_to_demonstrate = link_to_demonstrate
        self.rules = []

    def add_rule(self, rule):
        self.rules.extend(rule)

    def remove_rule(self, rule):
        if rule in self.rules:
            self.rules.remove(rule)

    def search_in_precedents_implies(self, link):
        for precedent in self.precedents_list:
            for imply in precedent.get_implies_list():
                if imply.get_consequence().compare_links(link):
                    return imply.get_rules_list()

    def deduce_recollections(self):
        flag = False
        for link in self.object_description.get_link_list():
            if self.link_to_demonstrate.compare_links(link):
                flag = True
        if not flag:
            print "Link to demonstrate not in object description."
        else:
            for implies in self.object_description.get_implies_list():
                if implies.get_consequence().compare_links(self.link_to_demonstrate):
                    rules_list = implies.get_rules_list()

                    old_list = []
                    while old_list != rules_list:
                        old_list = []
                        old_list.extend(rules_list)

                        for link_to_find in rules_list:

                            deductions = self.search_in_precedents_implies(link_to_find)
                            
                            if deductions:
                                self.add_rule(deductions)
                                self.remove_rule(link_to_find)

                        rules_list = self.rules

    def check_rules_on_unclassified(self):
        self.deduce_recollections()
        for rule in self.rules:
            flag = False
            for link in self.unclassified_object.get_link_list():
                if rule.compare_links(link):
                    flag = True
            if not flag:
                print "Object does not follow the rule: "
                print rule.to_string()
                return
        print "Object does follow all rules and is of the type searched for: "
        self.print_model()

    def print_model(self):
        print "Obtained model"
        print "IF:"
        for rule in self.rules:
            print rule.to_string()
        print "THEN:"
        print self.link_to_demonstrate.to_string()


if __name__ == "__main__":
    # A Cup description
    # This is a description of an object.
    # The object is a cup because it is stable and because it enables drinking.
    cup_link1 = Link("Is", "Object", "Cup")
    cup_link2 = Link("Is", "Object", "Stable")
    cup_link3 = Link("Enables", "Object", "Drinking")
    cup_imply = Implies([cup_link2, cup_link3], cup_link1)
    cup_object = Description([cup_link1, cup_link2, cup_link3], [cup_imply])


    # A Particular Object description
    # This is an exercise about a light object that is made of porcelain.
    # The object has a decoration, a concavity, and a handle.
    # The object's bottom is flat.  Show that the object is a cup.
    unclassified_link1 = Link("Has", "Object", "Bottom")
    unclassified_link2 = Link("Is", "Bottom", "Flat")
    unclassified_link3 = Link("Has", "Object", "Concavity")
    unclassified_link4 = Link("MadeOf", "Object", "Porcelain")
    unclassified_link5 = Link("Has", "Object", "Decoration")
    unclassified_link6 = Link("Is", "Object", "Light")
    unclassified_link7 = Link("Has", "Object", "Handle")
    unclassified_object = Description([unclassified_link1, unclassified_link2, unclassified_link3, unclassified_link4, unclassified_link5, unclassified_link6, unclassified_link7], [])


    # A Brick
    # This is a description of a brick.
    # The brick is stable because the brick's bottom is flat.
    # The brick is heavy.
    brick_link1 = Link("Has", "Object", "Bottom")
    brick_link2 = Link("Is", "Bottom", "Flat")
    brick_link3 = Link("Is", "Object", "Stable")
    brick_imply = Implies([brick_link1, brick_link2], brick_link3)
    brick_link4 = Link("Is", "Object", "Heavy")
    brick_object = Description([brick_link1, brick_link2, brick_link3, brick_link4], [brick_imply])


    # A Glass
    # This is a description of a glass.
    # The glass enables drinking because the glass carries liquids and because the glass is liftable.
    # The glass is pretty.
    glass_link1 = Link("Carries", "Object", "Liquids")
    glass_link2 = Link("Is", "Object", "Liftable")
    glass_link3 = Link("Enables", "Object", "Drinking")
    glass_imply = Implies([glass_link1, glass_link2], glass_link3)
    glass_link4 = Link("Is", "Object", "Pretty")
    glass_object = Description([glass_link1, glass_link2, glass_link3, glass_link4], [glass_imply])


    # A Briefcase
    # This is a description of a briefcase.
    # The briefcase is liftable because it has a handle and because it is light.
    # The briefcase is useful because it is a portable container for papers.
    briefcase_link1 = Link("Is", "Object", "Light")
    briefcase_link2 = Link("Has", "Object", "Handle")
    briefcase_link3 = Link("Is", "Object", "Liftable")
    briefcase_imply = Implies([briefcase_link1, briefcase_link2], briefcase_link3)
    briefcase_object = Description([briefcase_link1, briefcase_link2, briefcase_link3], [briefcase_imply])


    # A Bowl
    # This is a description of a bowl.
    # The bowl carries liquids because it has a concavity.
    # The bowl contains cherry soup.
    bowl_link1 = Link("Has", "Object", "Concavity")
    bowl_link2 = Link("Carries", "Object", "Liquids")
    bowl_imply = Implies([bowl_link1], bowl_link2)
    bowl_link3 = Link("Has", "Object", "CherrySoup")
    bowl_object = Description([bowl_link1, bowl_link2, bowl_link3], [bowl_imply])

    # Create the rules based on the previous information and classify the unknown object.
    model = Model(cup_object, unclassified_object, [brick_object, glass_object, briefcase_object, bowl_object], Link("Is", "Object", "Cup"))
    model.check_rules_on_unclassified()
