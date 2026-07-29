// Run as the body of POST /api/doc/:id/exec after confirming the target doc.
const { createShapeId, toRichText } = await import('tldraw')

const input = createShapeId('qiaomu-example-input')
const attention = createShapeId('qiaomu-example-attention')
const output = createShapeId('qiaomu-example-output')

editor.createShapes([
	{
		id: input,
		type: 'geo',
		x: 80,
		y: 160,
		props: { geo: 'rectangle', w: 220, h: 120, richText: toRichText('Input tokens') },
	},
	{
		id: attention,
		type: 'geo',
		x: 420,
		y: 160,
		props: { geo: 'rectangle', w: 260, h: 120, richText: toRichText('Attention') },
	},
	{
		id: output,
		type: 'geo',
		x: 800,
		y: 160,
		props: { geo: 'rectangle', w: 220, h: 120, richText: toRichText('Context') },
	},
])

const a = helpers.createArrowBetweenShapes(input, attention, {
	richText: toRichText('Q · Kᵀ'),
})
const b = helpers.createArrowBetweenShapes(attention, output, {
	richText: toRichText('softmax · V'),
})

editor.select(input, attention, output, a, b)
editor.zoomToFit()
const lints = helpers.getLints()
await helpers.saveDoc()

return { created: [input, attention, output, a, b], lints: lints.lints }
