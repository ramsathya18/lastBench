"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { Button, Card } from "@/components/ui";
import { apiFetch, ApiError } from "@/lib/api";
import { CourseDetail, Lesson } from "@/types/domain";

export default function LearnPage() {
  const { courseSlug, lessonSlug } = useParams<{ courseSlug: string; lessonSlug: string }>();
  const [course, setCourse] = useState<CourseDetail | null>(null);
  const [answer, setAnswer] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const orderedLessons = useMemo(() => course?.modules.flatMap((m) => m.lessons) ?? [], [course]);
  const lesson = useMemo(() => orderedLessons.find((l) => l.slug === lessonSlug), [orderedLessons, lessonSlug]);
  const currentIndex = lesson ? orderedLessons.findIndex((l) => l.id === lesson.id) : -1;
  const prevLesson = currentIndex > 0 ? orderedLessons[currentIndex - 1] : null;
  const nextLesson = currentIndex >= 0 && currentIndex < orderedLessons.length - 1 ? orderedLessons[currentIndex + 1] : null;

  useEffect(() => {
    apiFetch(`/courses/${courseSlug}`)
      .then(setCourse)
      .catch((err: ApiError) => setError(err.message));
  }, [courseSlug]);

  useEffect(() => {
    if (!lesson?.id) return;
    apiFetch(`/lessons/${lesson.id}/start`, { method: "POST" }).catch(() => undefined);
  }, [lesson?.id]);

  if (error) return <p className="text-red-600">{error}</p>;
  if (!course || !lesson) return <p>Loading...</p>;

  return (
    <div className="grid gap-4 md:grid-cols-[280px_1fr]">
      <aside className="rounded border bg-white p-3">
        {course.modules.map((m) => (
          <div key={m.id} className="mb-3">
            <p className="font-semibold">{m.title}</p>
            <ul className="mb-2 ml-4 list-disc text-sm">
              {m.lessons.map((l) => (
                <li key={l.id}>
                  <Link className={l.slug === lesson.slug ? "font-semibold text-blue-600" : ""} href={`/learn/${course.slug}/${l.slug}`}>
                    {l.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </aside>
      <section className="space-y-4">
        <Card>
          <h1 className="text-xl font-bold">{lesson.title}</h1>
          <article className="prose whitespace-pre-wrap">{lesson.content_markdown}</article>
        </Card>

        <div className="flex flex-wrap gap-2">
          <Button
            onClick={async () => {
              try {
                await apiFetch(`/lessons/${lesson.id}/complete`, { method: "POST" });
                setMessage("Lesson marked complete.");
              } catch (err) {
                setError((err as ApiError).message);
              }
            }}
          >
            Mark complete
          </Button>
          {prevLesson && (
            <Link className="rounded-md border px-3 py-2" href={`/learn/${course.slug}/${prevLesson.slug}`}>
              Previous
            </Link>
          )}
          {nextLesson && (
            <Link className="rounded-md border px-3 py-2" href={`/learn/${course.slug}/${nextLesson.slug}`}>
              Next
            </Link>
          )}
        </div>
        {message && <p className="text-sm text-emerald-700">{message}</p>}

        {lesson.lesson_type === "quiz" && <QuizPanel lesson={lesson} />}
        {lesson.lesson_type === "sandbox" && <SandboxPanel lesson={lesson} answer={answer} setAnswer={setAnswer} setMessage={setMessage} setError={setError} />}
      </section>
    </div>
  );
}

function QuizPanel({ lesson }: { lesson: Lesson }) {
  const [quiz, setQuiz] = useState<any>();
  const [selected, setSelected] = useState<Record<number, number>>({});
  const [result, setResult] = useState<string>("");

  useEffect(() => {
    apiFetch(`/lessons/${lesson.id}/quiz`)
      .then(setQuiz)
      .catch(() => undefined);
  }, [lesson.id]);

  if (!quiz) return null;

  return (
    <Card>
      <h3 className="font-semibold">{quiz.title}</h3>
      {quiz.questions.map((q: any) => (
        <div key={q.id} className="mb-2">
          <p>{q.question_text}</p>
          {q.options_json.map((o: string, i: number) => (
            <label className="mr-4" key={i}>
              <input type="radio" name={`q-${q.id}`} onChange={() => setSelected((s) => ({ ...s, [q.id]: i }))} /> {o}
            </label>
          ))}
        </div>
      ))}
      <Button
        onClick={async () => {
          const payload = {
            answers: Object.entries(selected).map(([qid, v]) => ({ question_id: Number(qid), selected_indexes: [v] })),
          };
          const res = await apiFetch(`/quizzes/${quiz.id}/submit`, { method: "POST", body: JSON.stringify(payload) });
          setResult(`Score ${res.score} (${res.passed ? "passed" : "not passed"})`);
        }}
      >
        Submit quiz
      </Button>
      {result && <p className="mt-2 text-sm text-blue-700">{result}</p>}
    </Card>
  );
}

function SandboxPanel({ lesson, answer, setAnswer, setMessage, setError }: { lesson: Lesson; answer: string; setAnswer: (value: string) => void; setMessage: (v: string) => void; setError: (v: string) => void }) {
  return (
    <Card>
      <h3 className="font-semibold">Prompt Sandbox</h3>
      <textarea className="h-36 w-full border p-2" value={answer} onChange={(e) => setAnswer(e.target.value)} />
      <div className="mt-2 flex gap-2">
        <Button
          onClick={async () => {
            try {
              const t = await apiFetch(`/lessons/${lesson.id}/sandbox`);
              const r = await apiFetch(`/sandbox/tasks/${t.id}/run`, { method: "POST", body: JSON.stringify({ submitted_content: answer }) });
              setMessage(`Sandbox result: ${r.score_or_result?.passed ? "passed" : "not passed"}`);
            } catch (err) {
              setError((err as ApiError).message);
            }
          }}
        >
          Run
        </Button>
        <Button className="bg-slate-700" onClick={() => setAnswer("")}>Reset</Button>
      </div>
    </Card>
  );
}
