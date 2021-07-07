import spacy
nlp = spacy.load('en_core_web_sm')


def apply(input):
    # Find named entities, phrases and concepts
    doc = nlp(input)
    ents = [{"text": entity.text, "entity": entity.label_} for entity in doc.ents]
    return "Entities {0}".format(ents)


if __name__ == "__main__":
    input_t = "The Mars Orbiter Mission (MOM), informally known as Mangalyaan, " \
              "was launched into Earth orbit on 5 November 2013 by the " \
              "Indian Space Research Organisation (ISRO) and has entered" \
              " Mars orbit on 24 September 2014. India thus became" \
              " the first country to enter Mars orbit on its first attempt. " \
              "It was completed at a record low cost of $74 million."
    print(apply(input_t))