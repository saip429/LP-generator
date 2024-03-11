"""
Temporary script to test the pipelines until backend server integration
"""

from content_recommender import ContentRecommender
from path_generator import LearningPathGenerator

course_title = ""
syllabus_list = ()
keyword = "I want to learn python"
with LearningPathGenerator(keyword=keyword, difficulty="beginner") as mylpg:
    course_title = mylpg.extract_keyword()
    print(course_title)
    syllabus_list = mylpg.generate_path()
    print(syllabus_list)

for module in syllabus_list:
    with ContentRecommender(module) as myrec:
        myrec.forward()
        url = myrec.get_urls()
        print(url)
