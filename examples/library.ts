export interface Document {
  name: string;
  title: string;
  tags: readonly string[];
}

export class Library {
  private readonly entries = new Map<string, Document>();

  // Return a copy so callers cannot reorder the stored collection.
  list(tag?: string): Document[] {
    const documents = [...this.entries.values()];
    return tag === undefined
      ? documents
      : documents.filter(document => document.tags.includes(tag));
  }

  add(document: Document): boolean {
    if (this.entries.has(document.name)) {
      return false;
    }
    this.entries.set(document.name, document);
    return true;
  }
}
