import re
from enum import Enum

class Colours(Enum):
    """
    A class to store the ANSI colour codes for text.

    Attributes:
        BLACK (str): The ANSI code for black text.
        RED (str): The ANSI code for red text.
        GREEN (str): The ANSI code for green text.
        YELLOW (str): The ANSI code for yellow text.
        BLUE (str): The ANSI code for blue text.
        MAGENTA (str): The ANSI code for magenta text.
        CYAN (str): The ANSI code for cyan text.
        WHITE (str): The ANSI code for white text.
        RESET_ALL (str): The ANSI code to reset all text formatting.
    
    Methods:
        __str__(): Returns the ANSI code for the colour.
        from_string(color): Tries to get the ANSI color code from the Colours enum.
        hex_to_ansi(hex_code): Converts a hexadecimal color code to an ANSI color code.
    """
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET_ALL = "\033[0m"
    
    def __str__(self) -> str:
        return self.value
    
    @staticmethod
    def from_string(color: str) -> str:
        """
        Tries to get the ANSI color code from the Colours enum.
        
        If the color is not in the Colours enum, it tries to convert the color to an ANSI color code.
        If the color is a hexadecimal color code, it converts it to an ANSI color code.
        
        Args:
            color (str): The color to get the ANSI code for.
            
        Returns:
            str: The ANSI color code for the color.
        
        """
        try:
            return Colours[color.upper()]
        except KeyError:
            # Handle hexadecimal color codes
            pattern = r"#(?P<hex>[A-Fa-f0-9]{6})"
            match = re.match(pattern, color)
            print(match)
            if match:
                # Convert the hexadecimal color code to an ANSI color code
                hex_code = match.group("hex")
                # You need to implement the hex_to_ansi method
                ansi_code = Colours.hex_to_ansi(hex_code)
                return ansi_code
            return Colours.WHITE
            
    @staticmethod
    def hex_to_ansi(hex_code: str) -> str:
        """
        This method converts a hexadecimal color code to an ANSI color code.
        
        Args:
            hex_code (str): The hexadecimal color code to convert.
            
        Returns:
            str: The ANSI color code for the hexadecimal color code.
        """
        return f"\033[38;2;{int(hex_code[:2], 16)};{int(hex_code[2:4], 16)};{int(hex_code[4:], 16)}m"


class ColouredText:
    """
    A class to represent a piece of text with a colour.

    Attributes:
        text (str): The text to store in the ColouredText object.
        colour (str): The colour to apply to the text.

    Methods:
        __init__(text, colour): The constructor for the ColouredText class.
        __str__(): Returns a string representation of the ColouredText object.
        __len__(): Returns the length of the text in the ColouredText object.

    """

    def __init__(self, text: str, colour: Colours):
        """
        The constructor for the ColouredText class.

        I recommend using the static method `parse_from_string` to create instances of this class.

        Args:
            text (str): The text to store in the ColouredText object.
            colour (str): The colour to apply to the text.  

        Returns:
            ColouredText: A new instance of the ColouredText class.
        """
        self.text = text
        self.colour = colour

    def __str__(self) -> str:
        """
        Returns a string representation of the ColouredText object.

        This method returns the text with the colour tags applied.

        Returns:
            str: The string representation of the ColouredText object.
        """
        return str(self.colour) + self.text + str(Colours.RESET_ALL)

    def __len__(self) -> int:
        """
        Returns the length of the text in the ColouredText object.

        Returns:
            int: The length of the text in the ColouredText object.
        """
        return len(self.text)


class ColouredTextList(list):
    """
    A class to represent a list of ColouredText objects.

    Attributes:
        texts (list[ColouredText]): The list of ColouredText objects stored in the ColouredTextList.

    Methods:
        __init__(texts): The constructor for the ColouredTextList class.
        __str__(): Returns a string representation of the ColouredTextList.
        __len__(): Returns the number of ColouredText objects in the list.
        text_length(): Returns the total length of all the texts in the list.
    """

    def __init__(self, texts):
        """
        The constructor for the ColouredTextList class.

        Args:
            texts (list[ColouredText]): The list of ColouredText objects to store in the ColouredTextList.

        Returns:
            ColouredTextList: A new instance of the ColouredTextList class.
        """
        super().__init__(texts)
        self.texts = texts

    def __str__(self) -> str:
        """
        Returns a string representation of the ColouredTextList.

        This method joins all the ColouredText objects in the list into a single string.

        Returns:
            str: The string representation of the ColouredTextList.
        """
        return "".join(str(text) for text in self)

    def __len__(self) -> int:
        """
        Returns the number of ColouredText objects in the list.

        Returns:
            int: The number of ColouredText objects in the list.
        """
        return super().__len__()

    def text_length(self) -> int:
        """
        Returns the total length of all the texts in the list.

        This method calculates the sum of the lengths of all the ColouredText objects in the list.
        This ignores the color tags when calculating the length.

        Returns:
            int: The total length of all the texts in the list.
        """
        self.texts = [text for text in self.texts]
        return sum(len(text) for text in self.texts)


@staticmethod
def parse_from_string(string: str) -> ColouredTextList:
    """
    Parses a string into a ColouredTextList.

    This method finds all the color tags in the string and creates a ColouredText object for each one.
    If a part of the string doesn't have a color tag, it creates a ColouredText object with the default color (white) for that part.

    Args:
        string (str): The string to parse.

    Returns:
        ColouredTextList: The parsed ColouredTextList.
    """
    pattern = r"\<(?P<color>\w+|\#\w{6})\>(?P<text>.+?)\<\/(?P=color)\>"
    matches = re.finditer(pattern, string)
    colored_texts = []
    prev_end = 0

    for match in matches:
        start = match.start()
        end = match.end()
        color = match.group("color").upper()
        text = match.group("text")

        if start > prev_end:
            colored_texts.append(ColouredText(string[prev_end:start], Colours.WHITE))
        prev_end = end

        if color.startswith('#'):
            colored_texts.append(ColouredText(text, Colours.hex_to_ansi(color[1:])))
        elif hasattr(Colours, color):
            colored_texts.append(ColouredText(text, getattr(Colours, color).value))
        else:
            colored_texts.append(ColouredText(text, Colours.WHITE.value))

    if prev_end < len(string):
        colored_texts.append(ColouredText(string[prev_end:], Colours.WHITE))

    return ColouredTextList(colored_texts)