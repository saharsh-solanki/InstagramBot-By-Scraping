from Bot import InitiateBot

bot = InitiateBot("username","password")
# bot.PerformLogin()
bot.setAndCheckCookie()
# followers = bot.GetFollowerList("saharsh_solanki_")
# print(bot.FollowAPersonById("49900008469"))
bot.FollowFollowerOfAPersonByUsername("tejuswi_")
# bot.ApproveAllPendingRequest()