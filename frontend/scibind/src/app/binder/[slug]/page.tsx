"use client";

import Head from "next/head";
import Header from "@/components/header";
import Toolbar from "@/components/toolbar";
import Editor from "@/components/editor";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Head>
        <title>SciBind</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="fixed top-0 w-full z-10">
        <Header />
        <Toolbar />
      </div>

      <div className="mt-28">
        <Editor />
      </div>
    </div>
  );
}
