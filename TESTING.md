# GENERIC TESTING FILE

To allow for higher quality development please test your game with this cases. If your game intentionally breaks these case i.e. allows the user to define a custom token, then ignore and move to the next case.

Feature: Tic-Tac-Toe Core Gameplay
  As a player
  I want to play a game of Tic-Tac-Toe
  So that I can try to beat my opponent

  Scenario: Starting a new game
    Given a new game of Tic-Tac-Toe is started
    Then the board should be 3x3 and completely empty
    And it should be player "X"'s turn

  Scenario: Making a valid move
    Given it is player "X"'s turn
    And the top-left square is empty
    When player "X" plays in the top-left square
    Then the top-left square should contain an "X"
    And it should become player "O"'s turn

  Scenario: Attempting to play on an occupied square
    Given the center square already contains an "X"
    And it is player "O"'s turn
    When player "O" attempts to play in the center square
    Then the game should display a "space occupied" error message
    And the center square should still contain an "X"
    And it should remain player "O"'s turn

  Scenario: Attempting to play outside the board boundaries
    Given it is player "X"'s turn
    When player "X" attempts to play at coordinate "Z9"
    Then the game should display an "invalid coordinate" error message
    And the board state should remain unchanged
    And it should remain player "X"'s turn

  Scenario: Winning the game with a horizontal line
    Given player "X" has pieces in the top-left and top-middle squares
    And it is player "X"'s turn
    When player "X" plays in the top-right square
    Then player "X" should be declared the winner
    And the game should end

  Scenario: Winning the game with a diagonal line
    Given player "O" has pieces in the top-left and center squares
    And it is player "O"'s turn
    When player "O" plays in the bottom-right square
    Then player "O" should be declared the winner
    And the game should end

  Scenario: The game ends in a draw
    Given there is only one empty square left on the board
    And neither player has 3-in-a-row
    And playing in the final square does not create a winning line for the current player
    When the current player plays in the final empty square
    Then the game should declare a draw
    And the game should end

  Scenario: Attempting to play after the game has ended
    Given the game has already ended in a victory for player "X"
    When player "O" attempts to play in an empty square
    Then the game should display a "game over" error message
    And the board state should remain unchanged
