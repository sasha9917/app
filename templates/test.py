# from app import app, db, Article
#
# with app.app_context():
#     db.session.query(Article).delete()
#     db.session.commit()
#     print("✅ Базу очищено!")
def two_sum(numbers, target):
    for number in numbers:
        if target - number in numbers:
            return numbers.index(target - number), numbers.index(number)


print(two_sum([8, 2, 4], 6))
