import poplib
from email import parser

pop_conn = poplib.POP3_SSL("mail.cock.li")
pop_conn.user("oilrobot@cock.li")
pop_conn.pass_("Invisible531")
# Get messages from server:
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
print(messages[0])
fsdf="\n".join([it.decode('utf-8') for it in messages[0][1]])
print(fsdf)
mobj=parser.Parser().parsestr(fsdf)
print(mobj)
print(mobj["subject"])
# with open("testmail.out", "w") as file:
#     for it in messages:
#         file.write(f"{it}\n")
# # Concat message pieces:
# messages = ["\n".join(mssg[1]) for mssg in messages]
# # Parse message intom an email object:
# messages = [parser.Parser().parsestr(mssg) for mssg in messages]
# for message in messages:
#     print(message["subject"])
pop_conn.quit()

