from transformers import pipeline, set_seed
import textwrap

print("Downloading model... (This takes about 30 seconds)")
generator = pipeline('text-generation', model='gpt2')
print("Model loaded! Ready to experiment.")


def test_temperature(temp_value):
    print(f"\n🧪 TESTING TEMPERATURE: {temp_value}")
    print("-" * 40)

    try:
        set_seed(42)

        result = generator(
            "The secret to a happy life is",
            max_new_tokens=50,
            num_return_sequences=1,
            temperature=temp_value,
            do_sample=True,
            pad_token_id=50256
        )


        generated_text = result[0]['generated_text']
        print(textwrap.fill(generated_text, width=80))

    except Exception as e:
        print(f"Error: {e}")



temperature = [0.1, 0.2, 0.8, 1.7, 2]
for t in temperature:
  test_temperature(t)