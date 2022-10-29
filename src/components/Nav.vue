<template>
  <section class= "h-screen  col start w-17 tl fixed bg-secondary fade-in-left pt-16 z-20">
    <Router-Link to="/">
      <Dark class="m-4 p-1 z-50 x2 scale-110" />
      <Ico icon="mdi-home" class="m-4 p-1 z-50 x2 scale-110" />
    </Router-Link>
    <RouterLink to="/crawl">
      <Ico icon="mdi-bug" class="mx-4 p-1 z-50 x2 scale-110"  />
    </RouterLink>
  </section>
</template>
