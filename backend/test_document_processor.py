from document_processor import extract_text


# Create a fictional TXT document
class TestFile:

    name = "sample.txt"

    def getvalue(self):
        return b"Patient admitted on 25 November 2026.\nLab report received."


# Test document extraction
file = TestFile()

result = extract_text(file)

print("MEDUSA-X DOCUMENT PROCESSOR TEST")
print("--------------------------------")

print("Extracted Document Text:")
print(result)

if "Patient admitted" in result:
    print("\nTEST PASSED!")
else:
    print("\nTEST FAILED!")