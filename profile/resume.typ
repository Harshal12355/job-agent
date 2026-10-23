// Renders one resume packet. Usage:
//   typst compile --root . profile/resume.typ out/base/resume.pdf --input packet=/profile/packets/base_lane_a.yaml
#let p = yaml(sys.inputs.at("packet", default: "/profile/packets/base_lane_a.yaml"))

#set document(title: p.name + " Resume", author: p.name)
#set page(paper: "us-letter", margin: (x: 0.55in, y: 0.45in))
// Liberation Sans ships in the Docker image; render there so every PDF uses the same font.
#set text(font: "Liberation Sans", size: 9.6pt)
#set par(leading: 0.5em, spacing: 0.55em)
#set list(indent: 0.4em, body-indent: 0.45em, spacing: 0.38em)

#let section(title) = {
  v(0.6em)
  block(below: 0.45em, stroke: (bottom: 0.5pt), inset: (bottom: 2pt), width: 100%,
    text(size: 10.2pt, weight: "bold", upper(title)))
}

#let entry(left-top, right-top, left-bottom: none, right-bottom: none) = {
  grid(
    columns: (1fr, auto),
    row-gutter: 0.35em,
    text(weight: "bold", left-top), right-top,
    ..if left-bottom != none { (emph(left-bottom), emph(right-bottom)) },
  )
}

#align(center, stack(spacing: 0.7em,
  text(size: 16pt, weight: "bold", p.name),
  text(size: 10.5pt, p.headline),
  text(size: 8.6pt, p.contact.join("  |  ")),
))

#section("Summary")
#p.summary

#section("Experience")
#for job in p.experience {
  entry(job.company, job.dates, left-bottom: job.title, right-bottom: job.location)
  list(..job.bullets.map(b => b.text))
  v(0.25em)
}

#section("Projects")
#for proj in p.projects {
  entry(proj.name, proj.url)
  list(..proj.bullets.map(b => b.text))
  v(0.15em)
}

#section("Education")
#for edu in p.education {
  entry(edu.school, edu.dates, left-bottom: edu.degree, right-bottom: edu.location)
  if "detail" in edu { list(edu.detail) }
  v(0.15em)
}

#section("Skills")
#for s in p.skills [
  *#s.label:* #s.items.join(", ") \
]
