import random
import string

import torch


def _generate_word(start_letter, model, tokenizer, max_length, temperature=1.0):

    # start met start token + letter seed (BELANGRIJK)
    start_token = tokenizer.encode("<s>").ids[0]
    letter_token = tokenizer.encode(start_letter).ids[0]

    generated_tokens = [start_token, letter_token]

    input_seq = torch.tensor([generated_tokens], dtype=torch.long)

    model.eval()
    hidden = model.init_hidden(input_seq)

    for _ in range(max_length - 2):
        with torch.no_grad():
            output, hidden = model(input_seq, hidden)

        logits = output.squeeze(0)[-1, :]
        probs = torch.softmax(logits / temperature, dim=-1)

        next_token = torch.multinomial(probs, 1).item()

        if next_token == tokenizer.token_to_id("<pad>"):
            break

        generated_tokens.append(next_token)

        # context behouden (niet alleen laatste token!)
        input_seq = torch.tensor([generated_tokens], dtype=torch.long)

    return tokenizer.decode(generated_tokens)


def sample_n(n: int, model, tokenizer, max_length=20, temperature=1.0) -> list[str]:
    output_words = []
    for _ in range(n):
        random_start_letter = random.choice(string.ascii_lowercase)
        new_word = _generate_word(
            random_start_letter,
            model,
            tokenizer,
            max_length=max_length,
            temperature=temperature,
        )
        output_words.append(new_word)
    return output_words
