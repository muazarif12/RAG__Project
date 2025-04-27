from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import textwrap

class HadithGenerator:
    def __init__(self, model_name="Qwen/Qwen2.5-3B-Instruct"):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype="auto",
            trust_remote_code=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            return_full_text=False,
            max_new_tokens=500,
            do_sample=False
        )
    
    def generate_response(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        output = self.generator(messages)
        return textwrap.fill(output[0]["generated_text"], width=80)