from aiogram import F, Router, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3

router = Router()
dp = Dispatcher()
db=sqlite3.connect('database.db', check_same_thread=False)
cursor=db.cursor()

test1 = KeyboardButton(text='абсолютно!')
#test2 = KeyboardButton(text='test2')
tests = ReplyKeyboardMarkup(keyboard=[[test1]], resize_keyboard=True)

quest1 = KeyboardButton(text='1')
quest2 = KeyboardButton(text='2')
quest3 = KeyboardButton(text='3')
quest4 = KeyboardButton(text='4')
quest = ReplyKeyboardMarkup(keyboard=[[quest1, quest2, quest3, quest4]], resize_keyboard=True)

questions = [
    "Льстит, что ты мне доверяешь. Давай начнем с того, как ты характеризуешь себя?",
    "Хм, я уже заинтригован. А что из перечисленного соответствует тебе?",
    "Думаю, мы с тобой схожи в этом. А что насчет твоего отношения к себе?",
    "Я понимаю тебя. А как ты чувствуешь себя в компании незнакомых людей?",
    "Думаю, мы бы точно нашли коннект, оказавшись в одной компании. А как ты ведешь себя в экстремальных ситуациях?",
    "Хотел бы я быть рядом с тобой в таких ситуациях. А теперь, представим: ты хочешь впервые зайти в Гештальт, но твой телефон сел, а адрес ты не помнишь. Как ты поступишь?",
    "А какое качество в себе ты считаешь наиболее сильным?",
    "Сейчас будет странный вопрос. Если бы ты был(а) фигурой, то какой?",
    "О, я тоже выбрал этот вариант. Хм, а если бы твоя любимая кружка скоропостижно разбилась?",
    "Наверное, если бы я не был ботом и у меня была бы кружка, то я сделал бы то же самое. Уверен, в твоей жизни уже были экзамены (мы ведь заведение 18+, как-никак). Если ты не смог(ла) подготовиться к экзамену, то как бы ты вышел(ла) из этой ситуации?(Если такой ситуации не было, просто представь)"
]

variants = [
    "1. Я люблю находиться в тени и занимать роль терпеливого наблюдателя, который неторопливо следит за происходящим\n2. Мое спокойствие и неторопливость напоминает мирную и тихую реку, что протекает среди солнечного поля\n3. Мне нужно все и сразу, я не могу усидеть на месте и страстно жажду приключений, которые наполнят жизнь яркими красками \n4. Испытываю неутолимую жажду познавать новое и раздвигать горизонты своего сознания",
    "1. Я не впадаю в панику. Мое сердце холодно, а разум чист. Я словно Байкал\n2. Мои требования от себя и окружающих людей довольно высоки. Я согласен иметь дело только с тем, что дает мне полную уверенность и безопасность\n3. Мое сердце безмерно большое, а нрав невероятно мягкий. Честно говоря, я могу проронить слезу от воспоминания о чем-то прекрасном и дорогом моему сердцу\n4. Я решаю все здесь и сейчас. Стоять на месте и сомневаться - не мой путь",
    "1. Я принимаю все свои плюсы и минусы и считаю себя достойным человеком\n2. Иногда мне кажется, что других людей мне легче любить, чем себя, хотела бы я научится любить и себя так же сильно\n3. Моя самооценка справедливо высокая, но не завышенная, я уверен(а) в себе \n4. Честно, все так запутано… не могу сказать точно, я ни в чем сейчас не уверен(а)",
    "1. Вполне комфортно, но мне нужно немного времени, чтобы присмотреться к окружающим и раскрыться по-настоящему \n2. Честно, не люблю большие незнакомые компании. Останусь молчаливым и робким наблюдателем\n3.  Люди вокруг не влияют на меня. Чувствую себя, как обычно комфортно\n4. Обожаю новые знакомства! Всегда с легкостью вольюсь в любую компанию и стану ее частью",
    "1. Я могу потеряться. Мне легче и безопаснее сделать также, как сделают другие люди\n2. Я впадаю в такой ступор, что ухожу в себя. Хочется грустить и плакать\n3. Мой ум трезвый. Взвешу все «за» и «против», прежде, чем принять решение\n4. Я легко впадаю в панику и могу допустить ошибку, приняв поспешное решение, после чего буду много думать об этом",
    "1. Я спрошу у прохожих \n2. Значит не судьба. Вернусь домой и пойду туда, когда буду точно знать, в каком направлении двигаться\n3. Я чувствую духовный коннект с Гештальтом, пойду по интуиции и точно найду\n4. Ой, я точно не пропаду. Да я и по мху смогу определить, куда мне идти. Найду свой метод",
    "1. Я обладаю похвальной рассудительностью, для меня нет не решаемых проблем\n2. Моему спокойствию позавидуют многие, даже в экстремальных ситуациях \n3. Я во всем вижу хорошее, мои взгляды крайне оптимистичны, на все в этой жизни можно смотреть с улыбкой \n4. Я вечный генератор энергии. Мне все по плечу, любые горы покрою",
    "1. Я четкий квадрат\n2. Обтекаемый круг\n3. Острый треугольник \n4. Однозначно непредсказуемый зигзаг",
    "1. Я подумаю, стоит ли пытаться ее чинить. Может, легче избавиться от нее и купить новую? Несмотря на то, что она мне дорога, у всего в жизни есть начало и конец\n2. Расстроюсь так сильно, что даже не сразу приступлю к уборке осколков, она была мне дорога \n3. Такое случается, не беда! Я попробую починить ее, ведь лучше попробовать, чем впасть в уныние \n4. Я настолько разозлюсь, что кину ее еще раз! Она специально разбилась, чтобы позлить? Как всегда.",
    "1. Решил(а) выкрутиться и вспомнить хотя бы что-то. Лучше приложить какое-то усилие, чем никакое, а вдруг повезёт?\n2. Было так грустно и все пошло на самотек, возможно получится, а возможно и нет\n3. Заболтать кого-то - не проблема. Главное не молчать и импровизировать, я точно смогу выйти из этой ситуации благодаря себе\n4. Все бесило и я вообще не пошел/не пошла, зачем вообще тратить на это силы?"
]

@router.message(Command("start"))
async def start_handler(msg: Message):
    if search_id(msg.chat.id):
        await msg.answer("Точно-точно?", reply_markup=tests)
        cursor.execute('INSERT INTO geshtalt (chat_id, current_test, test_num, count_1, count_2, count_3, count_4) VALUES (?, ?, ?, ?, ?, ?, ?)', (msg.chat.id, None, 0, 0, 0, 0, 0))
        db.commit()
    else:
        delete_user(msg.chat.id)
        await msg.answer("Точно-точно?", reply_markup=tests)
        cursor.execute('INSERT INTO geshtalt (chat_id, current_test, test_num, count_1, count_2, count_3, count_4) VALUES (?, ?, ?, ?, ?, ?, ?)', (msg.chat.id, None, 0, 0, 0, 0, 0))
        db.commit()

@router.message(Command("test"))
async def again_handler(msg: Message):
    if search_id(msg.chat.id):
        await msg.answer("Вы точно готовы пройти наш тест?", reply_markup=tests)
        cursor.execute('INSERT INTO geshtalt (chat_id, current_test, test_num, count_1, count_2, count_3, count_4) VALUES (?, ?, ?, ?, ?, ?, ?)', (msg.chat.id, None, 0, 0, 0, 0, 0))
        db.commit()
    else:
        await msg.answer("Вы уже проходите тест. Пожалуйста, завершите его или перезапустите бота.")

@router.message(F.text.lower().contains('абсолютно'))
async def test_type_handler(msg: Message):
    current_test = cursor.execute('SELECT current_test FROM geshtalt WHERE chat_id = ?', (msg.chat.id,)).fetchone()
    if current_test[0] is not None:
        await msg.answer("Вы уже проходите тест. Пожалуйста, завершите его или перезапустите бота.")
        return
    if msg.text.lower() == 'абсолютно!':  # type: ignore
        cursor.execute('UPDATE geshtalt SET current_test = ? WHERE chat_id = ?', (1, msg.chat.id))
        db.commit()
        await question_flow(msg)
    elif msg.text.lower() == 'test2':  # type: ignore
        await msg.answer("in develop")
    else:
        await msg.answer("not work")

async def question_flow(msg: Message):
    i = cursor.execute('SELECT test_num FROM geshtalt WHERE chat_id = ?', (msg.chat.id,)).fetchone()[0]
    if i < len(questions):
        await msg.answer(questions[i])
        await msg.answer(variants[i], reply_markup=quest)
    else:
        cnt1=cursor.execute('SELECT count_1 FROM geshtalt WHERE chat_id = ?', (msg.chat.id,)).fetchone()[0]
        cnt2=cursor.execute('SELECT count_2 FROM geshtalt WHERE chat_id = ?', (msg.chat.id,)).fetchone()[0]
        cnt3=cursor.execute('SELECT count_3 FROM geshtalt WHERE chat_id = ?', (msg.chat.id,)).fetchone()[0]
        cnt4=cursor.execute('SELECT count_4 FROM geshtalt WHERE chat_id = ?', (msg.chat.id,)).fetchone()[0]
        result={'1':cnt1,'2':cnt2,'3':cnt3,'4':cnt4}
        personality_res=max(result, key=result.get) # type: ignore
        if personality_res == '1':
            await msg.answer("Ммм, нравится сдержанность флегматика. Хотел бы я уметь также не тратить свои эмоции налево и направо, хотя бы иногда. Любишь постоянство и стабильность, понимаю. Хочу угостить тебя кое-какой настойкой. Думаю, тебе понравится «Умиротворение»",reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        elif personality_res == '2':
            await msg.answer("Хм, а ты смахиваешь на меланхолика. Тонкая и чувственная натура, предпочитающая медленное лавирование среди повседневных дел. Признаюсь честно, я тоже часто пропускаю слезу из-за небольших неурядиц. Это нормально и естественно, все мы люди. Вероятно, твоя коронная настойка - «Апатия»",reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        elif personality_res == '3':
            await msg.answer("Чувствую в тебе черты сангвиника, друг! Целеустремленность и энергия в сочетании с ювелирным контролем собственных эмоций. Иногда можешь опускать руки при долгих трудностях. Подними сейчас одну руку, позови бармена и попроси настойку «Увлеченность». Думаю, это то, что тебе нужно",reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        elif personality_res == '4':
            await msg.answer("Вау, да у нас здесь холерик собственной персоной! Человек - фейверк, «всё или ничего», верно? По-доброму завидую твоей энергии и активности, дружище. Пообщался с тобой и понял, твоя настойка - «эмоциональные качели/абьюзивные отношения»",reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        else:
            await msg.answer("что-то пошло не так, попробуйте перезапустить")
        delete_user(msg.chat.id)

@router.message(F.text.lower().contains('1') | F.text.lower().contains('2') | F.text.lower().contains('3') | F.text.lower().contains('4'))
async def answer_handler(msg: Message):
    current_test = cursor.execute('SELECT current_test FROM geshtalt WHERE chat_id = ?', (msg.chat.id,)).fetchone()[0]
    if current_test is None:
        await msg.answer("Вы точно готовы пройти наш тест?")
        return
    res = question_handler(msg.text.lower(), msg.chat.id) # type: ignore
    if not res:
        await msg.answer("Пожалуйста, выберите вариант ответа от 1 до 4")
    else:
        i = cursor.execute('SELECT test_num FROM geshtalt WHERE chat_id = ?', (msg.chat.id,)).fetchone()[0]
        cursor.execute('UPDATE geshtalt SET test_num = ? WHERE chat_id = ?', (i+1, msg.chat.id))
        db.commit()
        await question_flow(msg)

def question_handler(text, chat_id):
    if text == '1':
            tmp1 = cursor.execute('SELECT count_1 FROM geshtalt WHERE chat_id = ?', (chat_id,)).fetchone()[0]
            cursor.execute('UPDATE geshtalt SET count_1 = ? WHERE chat_id = ?', (tmp1+1, chat_id))
            db.commit()
            return True
    elif text == '2':
            tmp2 = cursor.execute('SELECT count_2 FROM geshtalt WHERE chat_id = ?', (chat_id,)).fetchone()[0]
            cursor.execute('UPDATE geshtalt SET count_2 = ? WHERE chat_id = ?', (tmp2+1, chat_id))
            db.commit()
            return True
    elif text == '3':
            tmp3 = cursor.execute('SELECT count_3 FROM geshtalt WHERE chat_id = ?', (chat_id,)).fetchone()[0]
            cursor.execute('UPDATE geshtalt SET count_3 = ? WHERE chat_id = ?', (tmp3+1, chat_id))
            db.commit()
            return True
    elif text == '4':
            tmp4 = cursor.execute('SELECT count_4 FROM geshtalt WHERE chat_id = ?', (chat_id,)).fetchone()[0]
            cursor.execute('UPDATE geshtalt SET count_4 = ? WHERE chat_id = ?', (tmp4+1, chat_id))
            db.commit()
            return True
    else:
        return False

def search_id(chat_id):
    is_new = cursor.execute('SELECT * FROM geshtalt WHERE chat_id = ?', (chat_id,)).fetchone()
    return is_new == None
    
def delete_user(chat_id):
    cursor.execute('DELETE FROM geshtalt WHERE chat_id = ?', (chat_id,))
    db.commit()