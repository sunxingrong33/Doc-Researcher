export interface Meme {
  _id: string;
  title: string;
  imageUrl: string;
  topText: string;
  bottomText: string;
  fontSize: number;
  textColor: string;
  strokeColor: string;
  generatedImageUrl?: string;
  createdAt: string;
}

export interface CreateMemeData {
  title: string;
  topText: string;
  bottomText: string;
  fontSize?: number;
  textColor?: string;
  strokeColor?: string;
  image: File;
}

export interface UpdateMemeData {
  title?: string;
  topText?: string;
  bottomText?: string;
  fontSize?: number;
  textColor?: string;
  strokeColor?: string;
}
