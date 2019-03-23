package main

import (
	"bytes"
	"context"
	"net/http"
	"strings"

	"github.com/graphql-go/graphql"
	"github.com/labstack/echo"
	"github.com/labstack/echo/middleware"
)

type ctxKey uint8

const (
	ctxAuthToken ctxKey = iota
	ctxClientIP  ctxKey = iota
)

var schema graphql.Schema

func init() {
	schema, _ = graphql.NewSchema(graphql.SchemaConfig{
		Query: graphql.NewObject(graphql.ObjectConfig{
			Name: "RootQuery",
			Fields: graphql.Fields{
				"me":          MeQuery,
				"post":        PostQuery,
				"postList":    PostListQuery,
				"snippet":     SnippetQuery,
				"snippetList": SnippetListQuery,
			},
		}),
		Mutation: graphql.NewObject(graphql.ObjectConfig{
			Name: "RootMutation",
			Fields: graphql.Fields{
				"createPost":    CreatePostMutation,
				"updatePost":    UpdatePostMutation,
				"createSnippet": CreateSnippetMutation,
				"updateSnippet": UpdateSnippetMutation,
			},
		}),
	})
}

func main() {
	e := echo.New()
	e.Any("/graphql", func(c echo.Context) error {
		var req string
		if c.Request().Method == "GET" {
			req = c.QueryParam("query")
		} else if c.Request().Method == "POST" {
			buf := new(bytes.Buffer)
			buf.ReadFrom(c.Request().Body)
			req = buf.String()
		}

		// Parse context for request.
		ctx := context.Background()
		ctx = context.WithValue(ctx, ctxClientIP, c.RealIP())
		if token := c.Request().Header.Get("Authorization"); strings.HasPrefix(token, "Bearer ") {
			ctx = context.WithValue(ctx, ctxAuthToken, token)
		}

		// Run query and return the result.
		result := graphql.Do(graphql.Params{
			Schema:        schema,
			RequestString: req,
			Context:       ctx,
		})

		return c.JSON(http.StatusOK, result)
	})

	e.Use(middleware.GzipWithConfig(middleware.GzipConfig{Level: 5}))
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"http://127.0.0.1:8080", "https://lynlab.co.kr"},
		AllowHeaders: []string{echo.HeaderOrigin, echo.HeaderContentType, echo.HeaderAccept, echo.HeaderAuthorization},
	}))
	e.Logger.Fatal(e.Start(":1323"))
}
