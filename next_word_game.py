"""
 Game of words

 Main function : play

 To test the game, call the test_the_game, which by default is called, will start
 an interactive play on the console
"""
BUCKET_OF_WORDS_FILE = 'words.txt'

CHARACTERS_SEEN = {}

SHOW_LEAKAGE = True # Set this to false if you do not want to see the next bug of words from which an answer is picked

class GameOverException(Exception):
  pass

def play(characters):
  global CHARACTERS_SEEN

  # return longest word given two words
  def word_length_comparator(word1, word2):
    if len(word1) > len(word2):
      return 1
    elif len(word1) == len(word2):
      return 0
    else:
      return -1

  # get next suitable character
  def get_next_suitable_character(characters, next_suitable_words):
    global CHARACTERS_SEEN
    # let's prune our dictionary
    pruned_words = [word.strip() for word in next_suitable_words if word.startswith(characters) and word != characters]

    try:
      # reset the chars seen
      CHARACTERS_SEEN = {}
      CHARACTERS_SEEN[characters] = pruned_words

      if SHOW_LEAKAGE:
        print "\t\t\t\t--START BUG_OF_WORDS--\n",  CHARACTERS_SEEN.values(), "\n\t\t\t\t--END BUG_OF_WORDS--\n"

      return pruned_words[0][len(characters)]
    except IndexError:
      raise GameOverException("Game Over")


  # first, let's if we have encountered these characters before
  for character_seen, character_seen_word_suggestions in CHARACTERS_SEEN.iteritems():
    if character_seen.startswith(characters) or characters.startswith(character_seen):
      return get_next_suitable_character(characters, character_seen_word_suggestions)

  # this is the first time we are encountering these characters
  with open(BUCKET_OF_WORDS_FILE) as word_corpus:
    bucket_of_words = word_corpus.readlines()
    bucket_of_words = [word.strip() for word in bucket_of_words if word.startswith(characters) and word != characters]

    if characters == '':
      """
        if it's the computer initiating the game, biase the game to provide a scenario
        where the user is led to providing words where he/she will be forced to provide
        the last character
      """
      words_with_chances = [word for word in bucket_of_words if len(word) % 2 == 0]
    else:
      """
      It's the user initiating the game, biase the game to prevent
      a scenario where I'll be forced to provide the last character by excluding
      words with even character count
      """
      words_with_chances = [word for word in bucket_of_words if len(word) % 2 != 0]

    # sort as per length
    words_with_chances.sort(cmp = lambda word1, word2: word_length_comparator(word1, word2))

    CHARACTERS_SEEN[characters] = words_with_chances

    return get_next_suitable_character(characters, words_with_chances)


# function to test the game
def test_the_game():
  word = ""
  while(True):
    try:
      print "\nCharacters entered so far are: {}\n \t ".format(word)
      print "\n\t\t\tUser Playing"
      user_char = raw_input("\tEnter next character: ")
      word = word + user_char
      print "\tUser Play Result: [Char: {}], [Word: {}]".format(user_char, word)

      print "\n\t\t\tComputer Playing"
      comp_char = play(word)
      word = word + comp_char

      print "\tComputer Play Result: [Char: {}], [Word: {}]".format(comp_char, word)
    except GameOverException:
      print "Game over, word formed is: {}".format(word)
      break

test_the_game()

