export type LessonType = "article" | "quiz" | "exercise" | "sandbox";

export interface Lesson {
  id: number;
  module_id: number;
  title: string;
  slug: string;
  summary: string;
  lesson_type: LessonType;
  content_markdown: string;
  estimated_minutes: number;
  sort_order: number;
  status: "draft" | "published";
}

export interface Module {
  id: number;
  course_id: number;
  title: string;
  description: string;
  sort_order: number;
  lessons: Lesson[];
}

export interface Course {
  id: number;
  title: string;
  slug: string;
  description: string;
  difficulty: string;
  estimated_minutes: number;
  tags: string[];
  thumbnail_url: string;
  status: "draft" | "published";
}

export interface CourseDetail extends Course {
  modules: Module[];
}
