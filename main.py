from resume import ResumeParser

def main():
    parser = ResumeParser()
    resume = parser.extract_text("resume.pdf")
    print(resume)


if __name__ == "__main__":
    main()