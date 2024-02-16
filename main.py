import json

import fastapi
import psycopg2

app = fastapi.FastAPI()


@app.post("/api/v0/evaluate")
def evaluate():
    return fastapi.responses.JSONResponse({"payload": 1.02})


@app.post("/api/v0/quiz")
def add_quiz():
    return fastapi.responses.JSONResponse({"payload": True})


def read_ff():
    quizes = {}
    with open("questions.txt", "r", encoding="Utf-8") as f:
        group_start = False
        group_name = ""
        for line in f:
            line = line.strip()
            if not line:
                group_start = True
                continue
            elif group_start:
                group_start = False
                group_name = line
                quizes[group_name] = []
            elif group_name:
                quiz, ans = line.split("=")
                quizes[group_name].append((quiz.strip(), int(ans.strip())))

    return quizes


if __name__ == '__main__':
    # quizes = read_ff()
    # print(quizes)

    conn = psycopg2.connect("dbname='mydb' user='JACKY' host='localhost' password='wyq020222'")
    # cur = conn.cursor()

    # # create quiz level
    # # level_sql = "insert into quiz_level (name) values (%s)"
    # # cur.executemany(level_sql,[(k,)for k in quizes.keys()])
    # # conn.commit()
    # # cur.close()
    #
    # cur = conn.cursor()
    # select_all_level_sql = "select level_id, name from quiz_level"
    # cur.execute(select_all_level_sql)
    # levels = cur.fetchall()
    # cur.close()
    #
    # levels = {name: id for id, name in levels}
    #
    # # insert quiz
    # data = []
    # for k, v in quizes.items():
    #     for q, a in v:
    #         data.append((q, a, levels[k]))
    #
    # print(data)
    #
    # cur = conn.cursor()
    # insert_sql = "insert into quiz (quiz, ans, level) values (%s,%s,%s)"
    # cur.executemany(insert_sql, data)
    # conn.commit()
    # cur.close()

    # # insert hidden parent
    # cur = conn.cursor()
    # insert_parent_sql = "insert into parent(name) values (%s)"
    # cur.executemany(insert_parent_sql, [("DEFAULT_PARENT_NAME",)])
    # conn.commit()
    #
    # cur.close()

    # insert random child

    # # get parent id
    # cur = conn.cursor()
    # get_parent_sql = "select pid from parent"
    # cur.execute(get_parent_sql)
    # pid = cur.fetchone()[0]
    #
    # # generate correct rate for each quiz
    # cur = conn.cursor()
    # cur.execute("select quiz_id from quiz")
    # quizzes = cur.fetchall()
    # quizzes = {q:random.random() for q in quizzes }
    #
    # for i in range(500):
    #     cur = conn.cursor()
    #     cur.execute("insert into children(cid,parent_id,name) values (%s,%s,%s)",(i, pid, f"CHILD{i}"))
    #     conn.commit()
    #
    #     res = []
    #     for quiz,cor in quizzes.items():
    #         res.append((i,quiz,random.random()>cor))
    #
    #     cur.executemany("insert into ans_records(cid,qid,correct) values (%s,%s,%s)",res)
    #     conn.commit()
    #
    # cur.close()
    # query quiz ans
    # cur = conn.cursor()
    # with open("ans.jsonline", "w", encoding="Utf-8") as f:
    #     # query all quiz
    #     cur.execute("select cid from children")
    #     qids = cur.fetchall()
    #
    #     for qid in qids:
    #         # get all ans record
    #         cur.execute("select qid,correct from ans_records where cid = %s", (qid,))
    #
    #         ans = cur.fetchall()
    #         data = {"subject_id": str(qid[0]), "responses": dict([(str(cid), cor) for cid, cor in ans])}
    #
    #         json.dump(data, f)
    #         f.write("\n")
    #         print(f"qid: {qid} DONE")
    cur = conn.cursor()
    with open("./output/3pl/best_parameters.json", "r", encoding="Utf-8") as f:
        parameters = json.load(f)
        id_to_child = parameters["subject_ids"]
        id_to_quiz = parameters["item_ids"]

        for idx, ability in enumerate(parameters["ability"]):
            child_id = id_to_child[str(idx)]
            cur.execute("UPDATE children SET ability=%s WHERE cid=%s", (ability, child_id))
        conn.commit()

        for idx, (diff, disc, lambdas) in enumerate(zip(parameters["diff"], parameters["disc"], parameters["lambdas"])):
            quiz_id = id_to_quiz[str(idx)]
            cur.execute("UPDATE quiz SET diff=%s, disc=%s, lambdas=%s WHERE quiz_id=%s", (diff, disc, lambdas, quiz_id))

        conn.commit()
    cur.close()