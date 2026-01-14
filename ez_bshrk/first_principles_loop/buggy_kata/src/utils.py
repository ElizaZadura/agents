"""
Utility functions for the buggy kata practice repo.
Each function contains an intentional bug for agent loop practice.
"""

import re

def reverse_string(s: str) -> str:
    """
    Reverse a string.
    
    Args:
        s: The string to reverse
        
    Returns:
        The reversed string
    """
    return s[::-1]  # Correctly reverses the entire string


def is_prime(n: int) -> bool:
    """
    Check if a number is prime.
    
    Args:
        n: The integer to check
        
    Returns:
        True if n is prime, False otherwise
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def find_max(items: list) -> any:
    """
    Find the maximum value in a list.
    
    Args:
        items: A list of comparable items
        
    Returns:
        The maximum value, or None if list is empty
    """
    if not items:
        return None
    
    result = items[0]
    for item in items[1:]:
        if item > result:  # Corrects the comparison to find max
            result = item
    return result


def word_count(text: str) -> int:
    """
    Count the number of words in a text.
    
    Args:
        text: The text to count words in
        
    Returns:
        The number of words
    """
    if not text:
        return 0
    # removes punctuation and splits by whitespace
    clean_text = re.sub(r'[\W_]+', ' ', text)  
    words = clean_text.split()  # Splits considering whitespaces
    return len(words)
